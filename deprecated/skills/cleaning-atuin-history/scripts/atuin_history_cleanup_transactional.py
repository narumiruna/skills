# /// script
# dependencies = []
# ///
"""Transactional helpers for Atuin typo cleanup."""

from __future__ import annotations

import json
import os
import pty
import re
import select
import shlex
import sqlite3
import subprocess
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote as url_quote

HISTORY_ID_SELECT = """
SELECT id
FROM history
"""

TYPO_REVIEW_SEARCH_MODE = "prefix"
TYPO_DELETE_FILTER_MODE = "global"
TYPO_DELETE_TIME_WINDOW = timedelta(seconds=1)
DEFAULT_CLEANUP_BACKUP_DIRNAME = "cleanup-backups"
PTY_STEP_SETTLE_SECONDS = 0.25
PTY_COMMAND_TIMEOUT_SECONDS = 10.0


class CleanupError(RuntimeError):
    """User-facing transactional cleanup failure."""


def shell_quote(value: str) -> str:
    """Return a shell-safe token."""
    return shlex.quote(value)


def build_shell_command(parts: list[str]) -> str:
    """Render a list of argv parts as a shell-ready command string."""
    return " ".join(shell_quote(part) for part in parts)


def read_history_ids(db_path: Path) -> set[str]:
    """Read the raw row ids from Atuin history."""
    sqlite_uri = f"file:{url_quote(str(db_path))}?mode=ro"
    try:
        connection = sqlite3.connect(sqlite_uri, uri=True)
    except sqlite3.Error as exc:
        raise CleanupError(f"Failed to open SQLite database: {exc}") from exc

    try:
        try:
            rows = connection.execute(HISTORY_ID_SELECT)
        except sqlite3.Error as exc:
            raise CleanupError(f"Failed to read Atuin history ids: {exc}") from exc
        return {str(row[0]) for row in rows}
    finally:
        connection.close()


def sqlite_backup(source: Path, destination: Path) -> None:
    """Create a consistent SQLite snapshot using the backup API."""
    destination.parent.mkdir(parents=True, exist_ok=True)

    source_uri = f"file:{url_quote(str(source))}?mode=ro"
    try:
        source_connection = sqlite3.connect(source_uri, uri=True)
        destination_connection = sqlite3.connect(destination)
    except sqlite3.Error as exc:
        raise CleanupError(f"Failed to open SQLite backup connections: {exc}") from exc

    try:
        source_connection.backup(destination_connection)
    except sqlite3.Error as exc:
        raise CleanupError(f"Failed to back up SQLite database: {exc}") from exc
    finally:
        destination_connection.close()
        source_connection.close()


def write_json_report(path: Path, payload: dict[str, Any]) -> None:
    """Write a JSON report to disk."""
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def resolve_backup_dir(db_path: Path, explicit_dir: str | None) -> Path:
    """Resolve the cleanup backup directory."""
    if explicit_dir:
        backup_dir = Path(explicit_dir).expanduser()
    else:
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%SZ")
        backup_dir = db_path.parent / DEFAULT_CLEANUP_BACKUP_DIRNAME / timestamp

    backup_dir = backup_dir.resolve()
    if backup_dir.exists():
        raise CleanupError(f"Backup directory already exists: {backup_dir}")
    backup_dir.mkdir(parents=True, exist_ok=False)
    return backup_dir


def run_cli_command(
    parts: list[str],
    *,
    check: bool = True,
    capture_output: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess[str]:
    """Run a command and surface a concise user-facing error on failure."""
    result = subprocess.run(
        parts,
        check=False,
        capture_output=capture_output,
        text=text,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise CleanupError(f"`{build_shell_command(parts)}` failed: {stderr}")
    return result


def parse_remote_sync_status(raw_output: str) -> dict[str, str]:
    """Extract the configured remote status fields from `atuin status`."""
    section: str | None = None
    remote: dict[str, str] = {}

    for line in raw_output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            section = stripped.strip("[]").lower()
            continue
        if section != "remote" or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        remote[key.strip().lower()] = value.strip()

    address = remote.get("address")
    username = remote.get("username")
    if not address or not username:
        raise CleanupError(
            "Atuin remote sync is not configured or the current user is not logged in."
        )
    return {"address": address, "username": username}


def get_remote_sync_status() -> dict[str, str]:
    """Read and validate the current Atuin remote sync configuration."""
    result = run_cli_command(["atuin", "status"])
    return parse_remote_sync_status(result.stdout)


def parse_current_host_uuid(raw_output: str) -> str:
    """Extract the current host UUID from `atuin store status`."""
    match = re.search(
        r"^host:\s+([0-9a-f-]+)\s+<-\s+CURRENT HOST$",
        raw_output,
        re.MULTILINE,
    )
    if match is None:
        raise CleanupError(
            "Could not determine the current host UUID from `atuin store status`."
        )
    return match.group(1)


def get_current_host_uuid() -> str:
    """Return the current Atuin host UUID."""
    result = run_cli_command(["atuin", "store", "status"])
    return parse_current_host_uuid(result.stdout)


def parse_candidate_timestamp(value: Any) -> datetime:
    """Parse ISO timestamps from the audit output."""
    raw = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise CleanupError(f"Invalid candidate timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def candidate_delete_window(candidate: dict[str, Any]) -> tuple[datetime, datetime]:
    """Return the narrow timestamp window used for typo deletion."""
    timestamp = parse_candidate_timestamp(candidate["timestamp"])
    return (
        timestamp - TYPO_DELETE_TIME_WINDOW,
        timestamp + TYPO_DELETE_TIME_WINDOW,
    )


def entry_matches_cleanup_candidate(
    entry: Any,
    candidate: dict[str, Any],
    *,
    after_cutoff: datetime,
    before_cutoff: datetime,
) -> bool:
    """Apply the cleanup search filters in Python before choosing a delete path."""
    if entry.timestamp is None:
        return False
    if entry.timestamp < after_cutoff or entry.timestamp > before_cutoff:
        return False
    if not entry.command.startswith(candidate["original_command"]):
        return False

    cwd = candidate["cwd"]
    if cwd and cwd != "unknown" and entry.cwd != cwd:
        return False

    exit_code = candidate["previous_exit_code"]
    if exit_code is not None and entry.exit_code != exit_code:
        return False

    return True


def build_cleanup_search_parts(
    candidate: dict[str, Any],
    *,
    interactive: bool,
    delete: bool,
) -> list[str]:
    """Build a deterministic Atuin search command for typo cleanup."""
    after_cutoff, before_cutoff = candidate_delete_window(candidate)
    parts = ["atuin", "search"]
    if interactive:
        parts.append("-i")
    if delete:
        parts.append("--delete")

    parts.extend(
        [
            "--filter-mode",
            TYPO_DELETE_FILTER_MODE,
            "--search-mode",
            TYPO_REVIEW_SEARCH_MODE,
            "--after",
            after_cutoff.isoformat(),
            "--before",
            before_cutoff.isoformat(),
        ]
    )

    if candidate["cwd"] and candidate["cwd"] != "unknown":
        parts.extend(["--cwd", candidate["cwd"]])
    if candidate["previous_exit_code"] is not None:
        parts.extend(["--exit", str(candidate["previous_exit_code"])])

    parts.append(candidate["original_command"])
    return parts


def build_cleanup_plan(
    candidates: list[dict[str, Any]],
    entries: list[Any],
) -> list[dict[str, Any]]:
    """Route each candidate through a strict fast path or the TUI fallback."""
    plan: list[dict[str, Any]] = []

    for candidate in candidates:
        after_cutoff, before_cutoff = candidate_delete_window(candidate)
        matching_entries = sorted(
            [
                entry
                for entry in entries
                if entry_matches_cleanup_candidate(
                    entry,
                    candidate,
                    after_cutoff=after_cutoff,
                    before_cutoff=before_cutoff,
                )
            ],
            key=lambda entry: (
                entry.timestamp or datetime.min.replace(tzinfo=UTC),
                entry.id,
            ),
        )
        matching_ids = [entry.id for entry in matching_entries]
        if candidate["id"] not in matching_ids:
            raise CleanupError(
                f"Could not re-locate typo candidate {candidate['id']} before deletion."
            )

        target_index = matching_ids.index(candidate["id"])
        move_up = len(matching_ids) - target_index - 1
        route = "fast" if len(matching_ids) == 1 else "interactive"
        command_parts = build_cleanup_search_parts(
            candidate,
            interactive=route == "interactive",
            delete=route == "fast",
        )

        plan.append(
            {
                "id": candidate["id"],
                "timestamp": candidate["timestamp"],
                "cwd": candidate["cwd"],
                "original_command": candidate["original_command"],
                "route": route,
                "match_count": len(matching_ids),
                "match_ids": matching_ids,
                "move_up": move_up,
                "after_iso": after_cutoff.isoformat(),
                "before_iso": before_cutoff.isoformat(),
                "command": build_shell_command(command_parts),
                "command_parts": command_parts,
            }
        )

    return plan


def read_pty_output(master_fd: int, timeout_seconds: float) -> bytes:
    """Drain whatever the child TTY has emitted for a short burst."""
    chunks: list[bytes] = []
    deadline = time.monotonic() + timeout_seconds

    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break

        ready, _, _ = select.select([master_fd], [], [], remaining)
        if not ready:
            break

        try:
            chunk = os.read(master_fd, 4096)
        except OSError:
            break
        if not chunk:
            break
        chunks.append(chunk)
        deadline = time.monotonic() + 0.05

    return b"".join(chunks)


def run_interactive_cleanup_delete(command_parts: list[str], *, move_up: int) -> None:
    """Drive Atuin's inspector deletion flow through a PTY."""
    master_fd, slave_fd = pty.openpty()
    process = subprocess.Popen(
        command_parts,
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        close_fds=True,
    )
    os.close(slave_fd)

    output = bytearray()
    try:
        output.extend(read_pty_output(master_fd, PTY_STEP_SETTLE_SECONDS))
        for _ in range(move_up):
            os.write(master_fd, b"\x1b[A")
            output.extend(read_pty_output(master_fd, PTY_STEP_SETTLE_SECONDS))

        os.write(master_fd, b"\x0f")
        output.extend(read_pty_output(master_fd, PTY_STEP_SETTLE_SECONDS))
        os.write(master_fd, b"\x04")
        output.extend(read_pty_output(master_fd, PTY_STEP_SETTLE_SECONDS))
        os.write(master_fd, b"\x1b")
        output.extend(read_pty_output(master_fd, PTY_STEP_SETTLE_SECONDS))

        try:
            process.wait(timeout=PTY_COMMAND_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired as exc:
            process.kill()
            raise CleanupError(
                f"`{build_shell_command(command_parts)}` timed out while driving the TUI inspector."
            ) from exc
    finally:
        os.close(master_fd)

    if process.returncode != 0:
        decoded = output.decode(errors="replace").strip()
        detail = decoded or f"exit code {process.returncode}"
        raise CleanupError(f"`{build_shell_command(command_parts)}` failed: {detail}")


def execute_cleanup_plan(plan: list[dict[str, Any]]) -> dict[str, int]:
    """Execute the planned typo cleanup commands."""
    fast_count = 0
    interactive_count = 0

    for item in plan:
        if item["route"] == "fast":
            run_cli_command(item["command_parts"])
            fast_count += 1
            continue

        run_interactive_cleanup_delete(item["command_parts"], move_up=item["move_up"])
        interactive_count += 1

    return {"fast_count": fast_count, "interactive_count": interactive_count}


def verify_cleanup_result(
    snapshot_db_path: Path,
    live_db_path: Path,
    *,
    target_ids: list[str],
    post_audit: dict[str, Any],
) -> dict[str, Any]:
    """Confirm intended removals while allowing concurrent history additions."""
    if post_audit["typos"]["candidate_count"] != 0:
        raise CleanupError(
            "Post-delete audit still found high-confidence typo candidates. "
            "Manual recovery may be required."
        )

    snapshot_ids = read_history_ids(snapshot_db_path)
    live_ids = read_history_ids(live_db_path)
    removed_ids = sorted(snapshot_ids - live_ids)
    added_ids = sorted(live_ids - snapshot_ids)

    target_id_set = set(target_ids)
    unexpected_removed_ids = sorted(set(removed_ids) - target_id_set)
    missing_removed_ids = sorted(target_id_set - set(removed_ids))
    if unexpected_removed_ids or missing_removed_ids:
        raise CleanupError(
            "Post-delete verification failed: "
            + f"unexpected_removed_ids={unexpected_removed_ids}, "
            + f"missing_removed_ids={missing_removed_ids}."
        )

    return {
        "removed_ids": removed_ids,
        "added_ids": added_ids,
        "target_ids": sorted(target_id_set),
    }


def rollback_cleanup(snapshot_db_path: Path, live_db_path: Path) -> list[str]:
    """Preserve live and snapshot databases for race-free manual recovery."""
    del snapshot_db_path, live_db_path
    return [
        "Skipped automatic whole-database rollback to avoid racing with concurrent "
        "history writes; the live database and backup were preserved for manual "
        "recovery."
    ]


def render_cleanup_report(result: dict[str, Any]) -> str:
    """Render a text summary for cleanup-typos."""
    if result["status"] == "noop":
        return "\n".join(
            [
                "Atuin typo cleanup",
                f"DB: {result['db_path']}",
                "No high-confidence typo candidates found.",
            ]
        )

    lines = [
        "Atuin typo cleanup",
        f"DB: {result['db_path']}",
        f"Backup dir: {result['backup_dir']}",
        f"Candidates deleted: {result['candidate_count']}",
        f"Fast path deletions: {result['fast_count']}",
        f"Interactive fallback deletions: {result['interactive_count']}",
        f"Remote: {result['remote']['username']} @ {result['remote']['address']}",
        f"Current host: {result['current_host']}",
        f"Removed ids: {len(result['verification']['removed_ids'])}",
        "Status: success",
    ]
    return "\n".join(lines)
