#!/usr/bin/env python3
"""Audit Atuin history for duplicates and typo-like retries."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import sqlite3
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote as url_quote

HISTORY_SELECT = """
SELECT id, timestamp, exit, command, cwd, session, hostname
FROM history
"""

RARE_TOKEN_MAX_FREQUENCY = 3
MIN_OVERLAP_PREFIX_OR_SUFFIX = 2
TEXT_DUPLICATE_GROUP_LIMIT = 20
TYPO_REVIEW_SEARCH_MODE = "prefix"
DEFAULT_CLEANUP_DUPKEEP = 3


class AuditError(RuntimeError):
    """User-facing audit failure."""


@dataclass(frozen=True, slots=True)
class HistoryEntry:
    """Subset of Atuin history fields used by this audit."""

    id: str
    timestamp: datetime | None
    exit_code: int | None
    command: str
    cwd: str
    session: str | None
    hostname: str | None


def shell_quote(value: str) -> str:
    """Return a shell-safe token."""
    return shlex.quote(value)


def build_shell_command(parts: list[str]) -> str:
    """Render a list of argv parts as a shell-ready command string."""
    return " ".join(shell_quote(part) for part in parts)


def build_cd_command(cwd: str) -> str | None:
    """Return a shell-safe cd helper when the cwd looks usable."""
    if not cwd or cwd == "unknown":
        return None
    return f"cd {shell_quote(cwd)}"


def build_typo_preview_command(command: str, cwd: str) -> str:
    """Build a narrow interactive review command for a typo candidate."""
    parts = ["atuin", "search", "-i", "--search-mode", TYPO_REVIEW_SEARCH_MODE]
    if cwd and cwd != "unknown":
        parts.extend(["--cwd", cwd])
    parts.append(command)
    return build_shell_command(parts)


def add_shared_history_scope_args(parser: argparse.ArgumentParser) -> None:
    """Add db and typo-scope arguments shared by audit and cleanup."""
    parser.add_argument("--db-path", help="Explicit path to Atuin history.db")
    parser.add_argument(
        "--before",
        default="now",
        help="Audit only rows at or before this timestamp. Accepts 'now', ISO-8601, or Unix epoch.",
    )
    parser.add_argument(
        "--typo-window-seconds",
        type=int,
        default=300,
        help="Maximum gap between a failed typo and the corrected retry.",
    )
    parser.add_argument(
        "--max-typos",
        type=int,
        default=20,
        help="Maximum typo candidates to return.",
    )


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Audit Atuin history for duplicates and typo-like retries."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit = subparsers.add_parser(
        "audit",
        help="Inspect Atuin history without mutating the database.",
    )
    add_shared_history_scope_args(audit)
    audit.add_argument(
        "--dupkeep",
        type=int,
        default=3,
        help="How many copies dedup should keep per (command, cwd, hostname) group.",
    )
    audit.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )

    return parser.parse_args(argv)


def normalize_epoch_seconds(raw_value: float) -> float:
    """Normalize seconds, milliseconds, microseconds, or nanoseconds to seconds."""
    absolute = abs(raw_value)
    if absolute >= 1_000_000_000_000_000_000:
        return raw_value / 1_000_000_000
    if absolute >= 1_000_000_000_000_000:
        return raw_value / 1_000_000
    if absolute >= 1_000_000_000_000:
        return raw_value / 1_000
    return raw_value


def parse_timestamp(value: Any) -> datetime | None:
    """Parse Atuin timestamps stored as ints, floats, or ISO strings."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(normalize_epoch_seconds(float(value)), tz=UTC)

    raw = value.decode() if isinstance(value, bytes) else str(value)
    raw = raw.strip()
    if not raw:
        return None

    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        return datetime.fromtimestamp(normalize_epoch_seconds(float(raw)), tz=UTC)

    normalized = raw.replace("Z", "+00:00")
    normalized = re.sub(r"\s+UTC$", "+00:00", normalized)
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def parse_before(value: str) -> datetime:
    """Parse the audit cutoff timestamp."""
    if value == "now":
        return datetime.now(tz=UTC)

    parsed = parse_timestamp(value)
    if parsed is None:
        raise AuditError(
            f"Unsupported --before value: {value!r}. Use 'now', ISO-8601, or Unix epoch."
        )
    return parsed


def parse_history_db_path(atuin_info_output: str) -> Path:
    """Best-effort parse of history.db from `atuin info`."""
    candidates: list[str] = []

    for line in atuin_info_output.splitlines():
        stripped = line.strip()
        if not stripped or ":" not in stripped:
            continue
        label, value = stripped.split(":", 1)
        normalized_label = re.sub(r"\s+", " ", label.lower())
        cleaned_value = value.strip().strip("'\"")
        if not cleaned_value:
            continue
        if "history" in normalized_label and (
            "db" in normalized_label
            or "database" in normalized_label
            or "path" in normalized_label
        ):
            candidates.append(cleaned_value)
        elif cleaned_value.endswith(".db") and "history" in normalized_label:
            candidates.append(cleaned_value)

    for candidate in candidates:
        path = Path(candidate).expanduser()
        if path.suffix == ".db":
            return path

    fallback_match = re.search(
        r"(?P<path>(?:~|/)[^\s'\"`]*history\.db)", atuin_info_output
    )
    if fallback_match:
        return Path(fallback_match.group("path")).expanduser()

    raise AuditError("Could not find history.db in `atuin info` output.")


def resolve_db_path(explicit_path: str | None) -> Path:
    """Resolve the SQLite database path from CLI args or `atuin info`."""
    if explicit_path:
        path = Path(explicit_path).expanduser()
    else:
        if shutil.which("atuin") is None:
            raise AuditError(
                "Atuin is not installed or not on PATH. Pass --db-path to audit a specific database."
            )
        result = subprocess.run(
            ["atuin", "info"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip() or "unknown error"
            raise AuditError(f"`atuin info` failed: {stderr}")
        path = parse_history_db_path(result.stdout)

    if not path.exists():
        raise AuditError(f"History database does not exist: {path}")
    if not path.is_file():
        raise AuditError(f"History database is not a file: {path}")
    return path.resolve()


def parse_exit_code(value: Any) -> int | None:
    """Normalize exit code values from SQLite."""
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def load_history_entries(
    db_path: Path, before_cutoff: datetime
) -> tuple[list[HistoryEntry], dict[str, int]]:
    """Load history rows from SQLite in read-only mode."""
    sqlite_uri = f"file:{url_quote(str(db_path))}?mode=ro"
    total_rows = 0
    skipped_unparsed_timestamp = 0
    excluded_after_before = 0
    entries: list[HistoryEntry] = []

    try:
        connection = sqlite3.connect(sqlite_uri, uri=True)
        connection.row_factory = sqlite3.Row
    except sqlite3.Error as exc:
        raise AuditError(f"Failed to open SQLite database: {exc}") from exc

    try:
        try:
            rows = connection.execute(HISTORY_SELECT)
        except sqlite3.Error as exc:
            raise AuditError(f"Failed to read Atuin history table: {exc}") from exc

        for row in rows:
            total_rows += 1
            timestamp = parse_timestamp(row["timestamp"])
            if timestamp is None:
                skipped_unparsed_timestamp += 1
                continue
            if timestamp > before_cutoff:
                excluded_after_before += 1
                continue

            command = str(row["command"] or "").strip()
            if not command:
                continue

            entries.append(
                HistoryEntry(
                    id=str(row["id"]),
                    timestamp=timestamp,
                    exit_code=parse_exit_code(row["exit"]),
                    command=command,
                    cwd=str(row["cwd"] or ""),
                    session=str(row["session"]) if row["session"] else None,
                    hostname=str(row["hostname"]) if row["hostname"] else None,
                )
            )
    finally:
        connection.close()

    stats = {
        "rows_total": total_rows,
        "rows_analyzed": len(entries),
        "rows_skipped_unparsed_timestamp": skipped_unparsed_timestamp,
        "rows_excluded_after_before": excluded_after_before,
    }
    return entries, stats


def split_command_tokens(command: str) -> list[str] | None:
    """Split a shell command into tokens."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return None
    return tokens or None


def looks_like_path_or_script(token: str) -> bool:
    """Exclude path-like and script-like command names."""
    if "/" in token or "\\" in token or "." in token:
        return True
    if token.startswith(("~", "./", "../")):
        return True
    return bool(re.match(r"^[A-Za-z]:[/\\]", token))


def is_adjacent_transposition(left: str, right: str) -> bool:
    """Return true when the two strings differ only by one adjacent swap."""
    if len(left) != len(right) or left == right:
        return False
    diffs = [
        index
        for index, (a_char, b_char) in enumerate(zip(left, right))
        if a_char != b_char
    ]
    if len(diffs) != 2:
        return False
    first, second = diffs
    if second != first + 1:
        return False
    return (
        left[first] == right[second]
        and left[second] == right[first]
        and left[:first] == right[:first]
        and left[second + 1 :] == right[second + 1 :]
    )


def is_one_edit_apart(left: str, right: str) -> bool:
    """Return true when the strings are one insertion, deletion, or substitution apart."""
    if left == right:
        return False
    left_length = len(left)
    right_length = len(right)
    if abs(left_length - right_length) > 1:
        return False

    if left_length == right_length:
        differences = sum(1 for a_char, b_char in zip(left, right) if a_char != b_char)
        return differences == 1

    if left_length > right_length:
        left, right = right, left
        left_length, right_length = right_length, left_length

    index_left = 0
    index_right = 0
    edits = 0
    while index_left < left_length and index_right < right_length:
        if left[index_left] == right[index_right]:
            index_left += 1
            index_right += 1
            continue
        edits += 1
        if edits > 1:
            return False
        index_right += 1
    return True


def common_prefix_length(left: str, right: str) -> int:
    """Count shared characters from the start."""
    count = 0
    for left_char, right_char in zip(left, right):
        if left_char != right_char:
            break
        count += 1
    return count


def common_suffix_length(left: str, right: str) -> int:
    """Count shared characters from the end."""
    count = 0
    for left_char, right_char in zip(reversed(left), reversed(right)):
        if left_char != right_char:
            break
        count += 1
    return count


def is_high_confidence_typo_token(typo_token: str, corrected_token: str) -> bool:
    """Return true only for conservative typo-like token changes."""
    if typo_token == corrected_token:
        return False
    if is_adjacent_transposition(typo_token, corrected_token):
        return True
    if not is_one_edit_apart(typo_token, corrected_token):
        return False
    if max(len(typo_token), len(corrected_token)) < 4:
        return False
    return (
        common_prefix_length(typo_token, corrected_token)
        >= MIN_OVERLAP_PREFIX_OR_SUFFIX
        or common_suffix_length(typo_token, corrected_token)
        >= MIN_OVERLAP_PREFIX_OR_SUFFIX
    )


def build_dedup_command(before_value: str, dupkeep: int, dry_run: bool) -> str:
    """Build the suggested Atuin dedup command."""
    parts = ["atuin", "history", "dedup"]
    if dry_run:
        parts.append("--dry-run")
    parts.extend(["--before", before_value, "--dupkeep", str(dupkeep)])
    return build_shell_command(parts)


def analyze_duplicates(
    entries: list[HistoryEntry], before_value: str, dupkeep: int
) -> dict[str, Any]:
    """Group duplicates by (command, cwd, hostname)."""
    grouped: dict[tuple[str, str, str | None], list[HistoryEntry]] = defaultdict(list)
    for entry in entries:
        grouped[(entry.command, entry.cwd, entry.hostname)].append(entry)

    groups: list[dict[str, Any]] = []
    for (command, cwd, hostname), group_entries in grouped.items():
        count = len(group_entries)
        if count <= dupkeep:
            continue
        latest_timestamp = max(
            entry.timestamp for entry in group_entries if entry.timestamp is not None
        )
        groups.append(
            {
                "command": command,
                "cwd": cwd,
                "hostname": hostname,
                "count": count,
                "deletable_count": count - dupkeep,
                "latest_timestamp": latest_timestamp.isoformat(),
            }
        )

    groups.sort(
        key=lambda item: (
            item["deletable_count"],
            item["count"],
            item["latest_timestamp"],
            item["command"],
        ),
        reverse=True,
    )

    return {
        "dupkeep": dupkeep,
        "group_count": len(groups),
        "deletable_count": sum(group["deletable_count"] for group in groups),
        "preview_command": build_dedup_command(before_value, dupkeep, dry_run=True),
        "apply_command": build_dedup_command(before_value, dupkeep, dry_run=False),
        "groups": groups,
    }


def analyze_typos(
    entries: list[HistoryEntry],
    typo_window_seconds: int,
    max_typos: int,
) -> dict[str, Any]:
    """Find conservative typo-like retry pairs."""
    tokenized_commands: dict[str, list[str]] = {}
    first_token_frequency: Counter[str] = Counter()

    for entry in entries:
        tokens = split_command_tokens(entry.command)
        if not tokens:
            continue
        tokenized_commands[entry.id] = tokens
        first_token_frequency[tokens[0]] += 1

    by_session: dict[str, list[HistoryEntry]] = defaultdict(list)
    for entry in entries:
        if entry.session:
            by_session[entry.session].append(entry)

    candidates: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for session_entries in by_session.values():
        session_entries.sort(
            key=lambda entry: (
                entry.timestamp or datetime.min.replace(tzinfo=UTC),
                entry.id,
            )
        )
        for previous, current in zip(session_entries, session_entries[1:]):
            if previous.id in seen_ids:
                continue
            if previous.timestamp is None or current.timestamp is None:
                continue

            delta_seconds = int(
                (current.timestamp - previous.timestamp).total_seconds()
            )
            if delta_seconds < 0 or delta_seconds > typo_window_seconds:
                continue
            if previous.exit_code in (None, 0):
                continue

            previous_tokens = tokenized_commands.get(previous.id)
            current_tokens = tokenized_commands.get(current.id)
            if not previous_tokens or not current_tokens:
                continue
            if len(previous_tokens) != len(current_tokens):
                continue
            if previous_tokens[1:] != current_tokens[1:]:
                continue

            typo_token = previous_tokens[0]
            corrected_token = current_tokens[0]
            if looks_like_path_or_script(typo_token) or looks_like_path_or_script(
                corrected_token
            ):
                continue

            typo_frequency = first_token_frequency[typo_token]
            corrected_frequency = first_token_frequency[corrected_token]
            if typo_frequency == 0 or typo_frequency > RARE_TOKEN_MAX_FREQUENCY:
                continue
            if corrected_frequency < typo_frequency * 5:
                continue
            if not is_high_confidence_typo_token(typo_token, corrected_token):
                continue

            query = previous.command
            reason = "; ".join(
                [
                    f"same session within {delta_seconds}s",
                    f"previous exit {previous.exit_code}",
                    "arguments unchanged after the command name",
                    f"token frequency {corrected_token}={corrected_frequency} vs {typo_token}={typo_frequency}",
                ]
            )

            candidates.append(
                {
                    "id": previous.id,
                    "timestamp": previous.timestamp.isoformat(),
                    "cwd": previous.cwd,
                    "cwd_shell_quoted": shell_quote(previous.cwd),
                    "cd_command": build_cd_command(previous.cwd),
                    "original_command": previous.command,
                    "suggested_command": current.command,
                    "reason": reason,
                    "preview_query": query,
                    "preview_query_shell_quoted": shell_quote(query),
                    # Always override the search mode for review. Users often
                    # configure skim/fuzzy search, and Atuin's `--delete`
                    # removes every matching row rather than a chosen id.
                    "preview_command": build_typo_preview_command(
                        previous.command, previous.cwd
                    ),
                    "time_delta_seconds": delta_seconds,
                    "previous_exit_code": previous.exit_code,
                    "session": previous.session,
                    "hostname": previous.hostname,
                    "typo_token": typo_token,
                    "corrected_token": corrected_token,
                    "typo_token_frequency": typo_frequency,
                    "corrected_token_frequency": corrected_frequency,
                }
            )
            seen_ids.add(previous.id)

    candidates.sort(
        key=lambda item: (item["timestamp"], item["id"]),
        reverse=True,
    )

    return {
        "window_seconds": typo_window_seconds,
        "candidate_count": len(candidates),
        "returned_count": min(len(candidates), max_typos),
        "candidates": candidates[:max_typos],
    }


def audit_history(
    db_path: str | Path | None,
    *,
    dupkeep: int,
    before: str,
    typo_window_seconds: int,
    max_typos: int,
) -> dict[str, Any]:
    """Run the audit and return a structured report."""
    if dupkeep < 1:
        raise AuditError("--dupkeep must be at least 1.")
    if typo_window_seconds < 1:
        raise AuditError("--typo-window-seconds must be at least 1.")
    if max_typos < 1:
        raise AuditError("--max-typos must be at least 1.")

    before_cutoff = parse_before(before)
    resolved_db_path = resolve_db_path(str(db_path) if db_path is not None else None)
    entries, stats = load_history_entries(resolved_db_path, before_cutoff)

    report = {
        "db_path": str(resolved_db_path),
        "scope": {
            "before": before,
            "before_iso": before_cutoff.isoformat(),
            "dupkeep": dupkeep,
            "typo_window_seconds": typo_window_seconds,
            "max_typos": max_typos,
        },
        "stats": stats,
        "duplicates": analyze_duplicates(entries, before_cutoff.isoformat(), dupkeep),
        "typos": analyze_typos(entries, typo_window_seconds, max_typos),
    }
    return report


def format_duplicates_section(duplicates: dict[str, Any]) -> list[str]:
    """Render the duplicate summary for text output."""
    lines = [
        "Duplicates",
        f"- Groups over dupkeep={duplicates['dupkeep']}: {duplicates['group_count']}",
        f"- Potential removals: {duplicates['deletable_count']}",
        f"- Preview: {duplicates['preview_command']}",
        f"- Apply: {duplicates['apply_command']}",
    ]

    groups: list[dict[str, Any]] = duplicates["groups"]
    if not groups:
        lines.append("- No duplicate groups exceed the current threshold.")
        return lines

    visible_groups = groups[:TEXT_DUPLICATE_GROUP_LIMIT]
    lines.append(f"- Matching groups (top {len(visible_groups)} by removable count):")
    for group in visible_groups:
        lines.append(
            "  "
            + f"{group['count']} copies ({group['deletable_count']} removable) | "
            + f"host={group['hostname'] or '-'} | cwd={group['cwd'] or '-'} | "
            + f"command={group['command']}"
        )
    if len(groups) > len(visible_groups):
        omitted = len(groups) - len(visible_groups)
        lines.append(f"  ... {omitted} more groups omitted from text output")
    return lines


def format_typos_section(typos: dict[str, Any]) -> list[str]:
    """Render the typo summary for text output."""
    lines = [
        "Typos",
        f"- Candidates shown: {typos['returned_count']} of {typos['candidate_count']}",
        f"- Window: {typos['window_seconds']}s",
    ]

    candidates: list[dict[str, Any]] = typos["candidates"]
    if not candidates:
        lines.append("- No high-confidence typo candidates found.")
        return lines

    for index, candidate in enumerate(candidates, start=1):
        lines.extend(
            [
                f"{index}. id={candidate['id']} @ {candidate['timestamp']}",
                f"   cwd: {candidate['cwd']}",
                f"   original: {candidate['original_command']}",
                f"   suggested: {candidate['suggested_command']}",
                f"   reason: {candidate['reason']}",
                f"   preview: {candidate['preview_command']}",
                "   inspector: run preview, press Ctrl+O, confirm the entry, then press Ctrl+D",
            ]
        )
        if candidate["cd_command"]:
            lines.insert(-2, f"   restore cwd: {candidate['cd_command']}")
    return lines


def render_text_report(report: dict[str, Any]) -> str:
    """Render the audit as plain text."""
    stats = report["stats"]
    lines = [
        "Atuin history audit",
        f"DB: {report['db_path']}",
        f"Rows analyzed: {stats['rows_analyzed']} of {stats['rows_total']} total",
        f"Skipped unparsed timestamps: {stats['rows_skipped_unparsed_timestamp']}",
        f"Excluded after cutoff: {stats['rows_excluded_after_before']}",
        "",
    ]
    lines.extend(format_duplicates_section(report["duplicates"]))
    lines.append("")
    lines.extend(format_typos_section(report["typos"]))
    return "\n".join(lines)


def cleanup_typos(
    db_path: str | Path | None,
    *,
    before: str,
    typo_window_seconds: int,
    max_typos: int,
    backup_dir: str | None,
) -> dict[str, Any]:
    """Run the transactional typo cleanup flow."""
    pre_audit = audit_history(
        db_path,
        dupkeep=DEFAULT_CLEANUP_DUPKEEP,
        before=before,
        typo_window_seconds=typo_window_seconds,
        max_typos=max_typos,
    )
    candidates = pre_audit["typos"]["candidates"]
    candidate_count = pre_audit["typos"]["candidate_count"]
    if candidate_count == 0:
        return {
            "status": "noop",
            "db_path": pre_audit["db_path"],
            "candidate_count": 0,
        }
    if pre_audit["typos"]["returned_count"] != candidate_count:
        raise AuditError(
            f"Found {candidate_count} typo candidates but --max-typos only allowed "
            f"{pre_audit['typos']['returned_count']}. Increase --max-typos or narrow --before."
        )

    import atuin_history_cleanup_transactional as transactional

    resolved_db_path = Path(pre_audit["db_path"])
    try:
        remote = transactional.get_remote_sync_status()
        current_host = transactional.get_current_host_uuid()
        backup_root = transactional.resolve_backup_dir(resolved_db_path, backup_dir)
    except transactional.CleanupError as exc:
        raise AuditError(str(exc)) from exc
    snapshot_path = backup_root / "history.db.before"
    rollback_warnings: list[str] = []
    mutation_started = False

    try:
        transactional.run_cli_command(
            ["atuin", "store", "push", "--tag", "history", "--host", current_host]
        )
        transactional.sqlite_backup(resolved_db_path, snapshot_path)
        transactional.write_json_report(backup_root / "pre_audit.json", pre_audit)

        before_cutoff = parse_before(before)
        entries, _ = load_history_entries(resolved_db_path, before_cutoff)
        plan = transactional.build_cleanup_plan(candidates, entries)
        transactional.write_json_report(
            backup_root / "plan.json",
            {
                "db_path": str(resolved_db_path),
                "backup_dir": str(backup_root),
                "candidate_count": len(plan),
                "plan": plan,
            },
        )

        mutation_started = True
        execution = transactional.execute_cleanup_plan(plan)
        post_audit = audit_history(
            resolved_db_path,
            dupkeep=DEFAULT_CLEANUP_DUPKEEP,
            before=before,
            typo_window_seconds=typo_window_seconds,
            max_typos=max_typos,
        )
        verification = transactional.verify_cleanup_result(
            snapshot_path,
            resolved_db_path,
            target_ids=[candidate["id"] for candidate in plan],
            post_audit=post_audit,
        )
        post_verify = {"post_audit": post_audit, "verification": verification}
        transactional.write_json_report(backup_root / "post_verify.json", post_verify)

        transactional.run_cli_command(["atuin", "sync"])

        return {
            "status": "success",
            "db_path": str(resolved_db_path),
            "backup_dir": str(backup_root),
            "candidate_count": len(plan),
            "fast_count": execution["fast_count"],
            "interactive_count": execution["interactive_count"],
            "remote": remote,
            "current_host": current_host,
            "verification": verification,
        }
    except (AuditError, transactional.CleanupError) as exc:
        if mutation_started and snapshot_path.exists():
            rollback_warnings = transactional.rollback_cleanup(
                snapshot_path, resolved_db_path
            )

        detail = str(exc)
        if rollback_warnings:
            detail += " Recovery notes: " + "; ".join(rollback_warnings)
        detail += f" Backup dir: {backup_root}"
        raise AuditError(detail) from exc


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    args = parse_cli_args(argv)
    try:
        if args.command != "audit":
            raise AuditError(f"Unsupported command: {args.command}")
        report = audit_history(
            args.db_path,
            dupkeep=args.dupkeep,
            before=args.before,
            typo_window_seconds=args.typo_window_seconds,
            max_typos=args.max_typos,
        )
    except AuditError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
