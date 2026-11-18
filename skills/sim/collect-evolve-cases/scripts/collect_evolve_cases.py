# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Collect local, reviewed evolve cases from Pi session v3 files."""

import argparse
import collections
import fcntl
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
import time

MAX_LINE = 2**20
MAX_FILE = 32 * MAX_LINE
SAFE_ID = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
SENSITIVE = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\bBearer\s+[^\s]+|"
    r"\b(?:password|passwd|secret|token|api[_ -]?key)\s*[:=]\s*\S+|"
    r"\b(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{12,}|AKIA[A-Z0-9]{16})\b|"
    r"[\w.+-]+@[\w.-]+\.[a-z]{2,}\b|"
    r"(?:^|[\s\"'`])(?:/(?:home|Users)/|[a-z]:\\Users\\)",
    re.IGNORECASE,
)


def safe_id(value):
    """Accept only bounded, single-component storage names."""
    if not isinstance(value, str) or len(value) > 80 or not SAFE_ID.fullmatch(value):
        raise ValueError("expected a lowercase project, benchmark, skill, or case ID")
    return value


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(data, *, canonical=False):
    if canonical:
        response = json.dumps(data, ensure_ascii=False, sort_keys=True, allow_nan=False)
    else:
        response = (
            json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        )
    return response.encode("utf-8")


def no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def reject_constant(_):
    raise ValueError("nonfinite JSON number")


def load_json(data):
    return json.loads(
        data, object_pairs_hook=no_duplicates, parse_constant=reject_constant
    )


def git_path(cwd, flag):
    """Resolve Git identity without using ambient repository overrides."""
    env = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    result = subprocess.run(
        ["git", "-C", str(cwd), "rev-parse", "--path-format=absolute", flag],
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
        check=False,
    )
    return (
        pathlib.Path(result.stdout.rstrip("\n")).resolve()
        if not result.returncode
        else None
    )


class Project:
    """Match stored session working directories to a single local project."""

    def __init__(self, args):
        root = (
            (args.project_root or pathlib.Path.cwd()).expanduser().resolve(strict=True)
        )
        if not root.is_dir():
            raise ValueError("project root must be a directory")
        common = git_path(root, "--git-common-dir")
        if common is None and args.project_root is None:
            raise ValueError("use --project-root for a non-Git project")
        self.is_git = common is not None
        self.root = git_path(root, "--show-toplevel") if self.is_git else root
        if self.root is None or self.root == pathlib.Path(self.root.anchor):
            raise ValueError("expected a scoped project directory")
        self.identity = str(common or root)
        self.aliases = tuple(
            alias.expanduser().resolve() for alias in args.previous_root
        )
        for alias in self.aliases:
            if alias == pathlib.Path(alias.anchor) or alias.exists():
                raise ValueError("--previous-root requires a missing, scoped old path")
        # A standard Git common directory has the same parent name from every worktree.
        name = (common.parent if common else root).name.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", name).strip("-")[:48].rstrip("-") or "project"
        self.id = safe_id(
            args.project_id or f"{slug}-{digest(os.fsencode(self.identity))[:12]}"
        )
        bound = self.binding_path
        if bound.exists() or bound.is_symlink():
            binding = read_object(bound)
            old_identity = binding.get("identity")
            previous = {
                str(alias / ".git" if self.is_git else alias) for alias in self.aliases
            }
            if binding.get("kind") != self.binding["kind"] or old_identity not in (
                self.identity,
                *previous,
            ):
                raise ValueError("project ID belongs to a different project")

    @property
    def binding_path(self):
        return pathlib.Path.home() / ".agents/sim" / self.id / "project.json"

    @property
    def binding(self):
        return {
            "kind": "git" if self.is_git else "directory",
            "identity": self.identity,
        }

    def contains(self, cwd):
        if not isinstance(cwd, str) or not pathlib.Path(cwd).is_absolute():
            return False
        path = pathlib.Path(cwd).resolve()
        if path.is_dir():
            if self.is_git:
                common = git_path(path, "--git-common-dir")
                return common is not None and str(common) == self.identity
            return (
                path.is_relative_to(self.root)
                and git_path(path, "--git-common-dir") is None
            )
        return any(path.is_relative_to(alias) for alias in self.aliases)


def session_files(root):
    """Enumerate regular files in the documented Pi layout, not symlink targets."""
    if not root.is_dir() or root.resolve() != root.absolute():
        raise ValueError("session root must be an existing path without symlinks")
    for directory in sorted(root.iterdir()):
        if directory.is_symlink() or not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.jsonl")):
            info = path.lstat()
            if stat.S_ISREG(info.st_mode):
                yield path, info.st_mtime


def regular_reader(path):
    """Open a file for reading without following a final symlink or blocking on a FIFO."""
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    if not stat.S_ISREG(os.fstat(fd).st_mode):
        os.close(fd)
        raise ValueError("expected a regular file")
    return os.fdopen(fd, "rb")


def read_object(path):
    if path.resolve() != path.absolute():
        raise ValueError("refusing a symlinked input path")
    with regular_reader(path) as file:
        data = file.read(MAX_FILE + 1)
    if len(data) > MAX_FILE:
        raise ValueError("JSON input exceeds the size limit")
    value = load_json(data)
    if not isinstance(value, dict):
        raise ValueError("expected a JSON object")
    return value


def read_line(file):
    raw = file.readline(MAX_LINE + 1)
    if len(raw) > MAX_LINE or (raw and not raw.endswith(b"\n")):
        raise ValueError("oversized or incomplete session entry")
    if not raw:
        return None
    entry = load_json(raw)
    if not isinstance(entry, dict):
        raise ValueError("expected an object on each session line")
    return entry


def read_header(path, project):
    with regular_reader(path) as file:
        header = read_line(file)
    if not header or header.get("type") != "session" or header.get("version") != 3:
        raise ValueError("unsupported session header")
    entry_id(header)
    return header if project.contains(header.get("cwd")) else None


def entry_id(entry):
    value = entry.get("id")
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value):
        raise ValueError("invalid session or entry ID")
    return value


def read_tree(path, header):
    entries = {}
    parents = set()
    with regular_reader(path) as file:
        if os.fstat(file.fileno()).st_size > MAX_FILE or read_line(file) != header:
            raise ValueError("oversized or changed session")
        while (entry := read_line(file)) is not None:
            if file.tell() > MAX_FILE:
                raise ValueError("oversized session")
            key = entry_id(entry)
            parent = entry.get("parentId")
            if (
                not isinstance(entry.get("type"), str)
                or "parentId" not in entry
                or key in entries
                or (
                    parent is not None
                    and (not isinstance(parent, str) or parent not in entries)
                )
            ):
                raise ValueError("invalid session tree")
            entries[key] = entry
            if parent is not None:
                parents.add(parent)
    return entries, sorted(entries.keys() - parents)


def message_text(entry):
    message = entry.get("message")
    if entry["type"] != "message" or not isinstance(message, dict):
        return None
    role, content = message.get("role"), message.get("content")
    if role not in ("user", "assistant"):
        return None
    if isinstance(content, list):
        if role == "user" and any(
            not isinstance(block, dict) or block.get("type") != "text"
            for block in content
        ):
            return ""
        content = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
            and isinstance(block.get("text"), str)
        )
    return content.strip() if isinstance(content, str) else ""


def turns(entries, leaf):
    """Return request/response windows and optional next user message on one branch."""
    path = []
    while leaf is not None:
        path.append(entries[leaf])
        leaf = entries[leaf]["parentId"]
    path.reverse()
    edited = {
        entry["targetId"]
        for entry in path
        if entry["type"] == "context_edit" and isinstance(entry.get("targetId"), str)
    }
    groups = []
    for entry in path:
        raw = message_text(entry)
        if raw is None:
            continue
        key = entry["id"]
        safe = (
            key not in edited
            and raw
            and len(raw) <= 12_000
            and not SENSITIVE.search(raw)
        )
        if entry["message"]["role"] == "user":
            groups.append([key, bool(safe), []])
        elif groups and safe:
            groups[-1][2].append(key)
    return {
        key: {
            "request": key,
            "responses": responses,
            "next_user": groups[i + 1][0]
            if i + 1 < len(groups) and groups[i + 1][1]
            else None,
        }
        for i, (key, safe, responses) in enumerate(groups)
        if safe and responses
    }


def scan(args, project):
    cutoff = time.time() - args.days * 86400
    skipped = collections.Counter()
    sessions = []
    matched = 0
    truncated = False
    for path, stamp in sorted(
        session_files(args.sessions), key=lambda item: (-item[1], item[0])
    ):
        if stamp < cutoff:
            skipped["outside_time_window"] += 1
            continue
        try:
            header = read_header(path, project)
            if header is None:
                skipped["outside_project"] += 1
                continue
            if matched == args.limit:
                truncated = True
                break
            matched += 1
            entries, leaves = read_tree(path, header)
            if len(leaves) != 1:
                skipped["ambiguous_or_empty_branch"] += 1
                cases = []
            else:
                cases = list(turns(entries, leaves[0]).values())
            sessions.append({"id": header["id"], "leaves": leaves, "candidates": cases})
        except (
            OSError,
            ValueError,
            RuntimeError,
            RecursionError,
            subprocess.TimeoutExpired,
        ):
            skipped["unreadable_or_unsupported"] += 1
    return {
        "project_id": project.id,
        "days": args.days,
        "limit": args.limit,
        "sessions": sessions,
        "skipped": dict(skipped),
        "truncated": truncated,
    }


def find_session(args, project):
    matches = []
    for path, _ in session_files(args.sessions):
        try:
            header = read_header(path, project)
        except (
            OSError,
            ValueError,
            RuntimeError,
            RecursionError,
            subprocess.TimeoutExpired,
        ):
            continue
        if header and header["id"] == args.session:
            matches.append((path, header))
    if len(matches) != 1:
        raise ValueError("session ID missing, out of scope, or ambiguous")
    return matches[0]


def private_dir(path):
    if path.resolve() != path.absolute():
        raise ValueError("refusing a symlinked output directory")
    # main() sets umask 077 for newly created parent directories as well.
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = path.stat()
    if info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("output directory must be owned by you and private (0700)")


def atomic_json(path, data):
    if path.is_symlink():
        raise ValueError("refusing a symlinked output file")
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
        temporary = pathlib.Path(file.name)
        try:
            file.write(json_bytes(data))
            file.flush()
            os.fsync(file.fileno())
            file.close()
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def draft(args, project):
    path, header = find_session(args, project)
    entries, leaves = read_tree(path, header)
    leaf = args.leaf or (leaves[0] if len(leaves) == 1 else None)
    if leaf not in leaves:
        raise ValueError("select one valid leaf with --leaf")
    choices = turns(entries, leaf)
    if not args.request:
        return {
            "session_id": args.session,
            "leaf": leaf,
            "candidates": list(choices.values()),
        }
    records = []
    for request in dict.fromkeys(args.request):
        if request not in choices:
            raise ValueError("selected request is not eligible on this branch")
        source = {"session_id": args.session, **choices[request]}
        identity = [args.session, request, source["responses"]]
        records.append(
            {
                "id": f"case-{digest(json_bytes(identity))[:16]}",
                "input": {"instruction": message_text(entries[request])},
                "expected": None,
                "source": source,
            }
        )
    directory = project.binding_path.parent / "drafts"
    private_dir(directory)
    batch = {
        "project_id": project.id,
        "project": project.binding,
        "benchmark_id": args.benchmark_id,
        "skill": args.skill,
        "cases": records,
    }
    fd, name = tempfile.mkstemp(prefix="evolve-", suffix=".json", dir=directory)
    os.close(fd)
    dest = pathlib.Path(name)
    try:
        atomic_json(dest, batch)
    except BaseException:
        dest.unlink(missing_ok=True)
        raise
    return {"draft": str(dest), "case_ids": [record["id"] for record in records]}


def existing(path, default):
    return read_object(path) if path.exists() or path.is_symlink() else default


def valid_sources(source):
    if not isinstance(source, dict) or set(source) != {
        "session_id",
        "request",
        "responses",
        "next_user",
    }:
        raise ValueError("invalid source metadata")
    responses = source["responses"]
    if not isinstance(responses, list) or not responses:
        raise ValueError("expected response entry IDs")
    for id_ in [source["session_id"], source["request"], *responses]:
        entry_id({"id": id_})
    if source["next_user"] is not None:
        entry_id({"id": source["next_user"]})
    return source


def draft_cases(args, project):
    path = args.draft.expanduser().absolute()
    if path.parent != project.binding_path.parent / "drafts" or path.resolve() != path:
        raise ValueError("select a private draft under this project's drafts directory")
    with regular_reader(path) as file:
        info = os.fstat(file.fileno())
        if info.st_uid != os.getuid() or info.st_mode & 0o077:
            raise ValueError("draft must be owned by you and private (0600)")
        raw = file.read(MAX_FILE + 1)
    if len(raw) > MAX_FILE or digest(raw) != args.sha256:
        raise ValueError("draft size or approved SHA-256 does not match")
    batch = load_json(raw)
    expected = {
        "project_id": project.id,
        "project": project.binding,
        "benchmark_id": args.benchmark_id,
        "skill": args.skill,
    }
    if not isinstance(batch, dict) or any(
        batch.get(key) != value for key, value in expected.items()
    ):
        raise ValueError(
            "draft does not match the specified project, benchmark, and skill"
        )
    entries = index_cases(batch)
    result = []
    for key in dict.fromkeys(args.case):
        record = entries.get(key)
        if record is None:
            raise ValueError("approved case ID is missing from draft")
        payload = {key: record.get(key) for key in ("id", "input", "expected")}
        for field in ("input", "expected"):
            value = payload[field]
            if not isinstance(value, dict) or not value:
                raise ValueError(
                    "selected cases require nonempty input and expected objects"
                )
        if SENSITIVE.search(json_bytes(payload).decode("utf-8")):
            raise ValueError("selected case may contain sensitive content")
        result.append((payload, valid_sources(record.get("source"))))
    return result


def index_cases(document):
    cases = document.get("cases")
    if not isinstance(cases, list):
        raise ValueError("expected a cases array")
    result = {}
    for case in cases:
        key = case.get("id") if isinstance(case, dict) else None
        if not isinstance(key, str) or not key or key in result:
            raise ValueError("invalid or duplicate case ID in case set")
        result[key] = case
    return result


def case_content(case):
    return digest(json_bytes([case.get("input"), case.get("expected")], canonical=True))


def source_key(source):
    return source["session_id"], source["request"], tuple(source["responses"])


def merge_cases(evolve, sources, candidates):
    existing_cases = index_cases(evolve)
    active = {
        key: valid_sources(value)
        for key, value in sources.items()
        if key in existing_cases
    }
    by_source = {source_key(value): key for key, value in active.items()}
    by_content = {case_content(case) for case in existing_cases.values()}
    added = []
    for case, source in candidates:
        key = case["id"]
        fingerprint = case_content(case)
        matching = existing_cases.get(key) or existing_cases.get(
            by_source.get(source_key(source))
        )
        if matching is not None and case_content(matching) != fingerprint:
            raise ValueError(
                "case ID or source has conflicting content; nothing imported"
            )
        if matching is not None or fingerprint in by_content:
            continue
        active[key] = source
        by_content.add(fingerprint)
        existing_cases[key] = case
        by_source[source_key(source)] = key
        added.append(key)
    return {**evolve, "cases": list(existing_cases.values())}, active, added


def import_cases(args, project):
    candidates = draft_cases(args, project)
    root = project.binding_path.parent
    private_dir(root)
    lock = os.open(
        root / ".collect.lock", os.O_CREAT | os.O_NOFOLLOW | os.O_RDWR, 0o600
    )
    try:
        if not stat.S_ISREG(os.fstat(lock).st_mode):
            raise ValueError("expected a regular project lock file")
        fcntl.flock(lock, fcntl.LOCK_EX)
        # Recheck the project binding with the lock held.
        project = Project(args)
        benchmark = root / "evals" / args.benchmark_id
        private_dir(benchmark)
        evolve_path = benchmark / "evolve/evolve.json"
        source_path = benchmark / "sources.json"
        prior = existing(evolve_path, {"cases": []})
        sources = existing(source_path, {"skill": args.skill, "cases": {}})
        if sources.get("skill") != args.skill or not isinstance(
            sources.get("cases"), dict
        ):
            raise ValueError(
                "benchmark sources belong to a different skill or are invalid"
            )
        evolve, index, added = merge_cases(prior, sources["cases"], candidates)
        result = {"evolve": str(evolve_path), "added": added, "backup": None}
        if not added:
            return result
        private_dir(evolve_path.parent)
        backups = benchmark / "backups"
        private_dir(backups)
        backup = pathlib.Path(tempfile.mkdtemp(prefix="import-", dir=backups))
        if evolve_path.exists():
            atomic_json(backup / "evolve.json", prior)
        if source_path.exists():
            atomic_json(backup / "sources.json", sources)
        atomic_json(root / "project.json", project.binding)
        atomic_json(source_path, {"skill": args.skill, "cases": index})
        atomic_json(evolve_path, evolve)
        return {**result, "backup": str(backup)}
    finally:
        os.close(lock)


def positive(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return number


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=pathlib.Path)
    parser.add_argument("--project-id", type=safe_id)
    parser.add_argument(
        "--previous-root", type=pathlib.Path, action="append", default=[]
    )
    parser.add_argument(
        "--sessions",
        type=pathlib.Path,
        default=pathlib.Path.home() / ".pi/agent/sessions",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser(
        "scan", help="list eligible session and entry IDs only"
    )
    listing.add_argument("--days", type=positive, default=30)
    listing.add_argument("--limit", type=positive, default=100)
    drafting = commands.add_parser(
        "draft", help="write a private draft from selected requests"
    )
    drafting.add_argument("--session", required=True)
    drafting.add_argument("--leaf")
    drafting.add_argument("--request", action="append", default=[])
    importing = commands.add_parser("import", help="merge explicitly approved cases")
    importing.add_argument("--draft", type=pathlib.Path, required=True)
    importing.add_argument("--sha256", required=True)
    importing.add_argument("--case", type=safe_id, action="append", required=True)
    for command in (drafting, importing):
        command.add_argument("--benchmark-id", type=safe_id, required=True)
        command.add_argument("--skill", type=safe_id, required=True)
    args = parser.parse_args()
    args.sessions = args.sessions.expanduser().absolute()
    return args


def main():
    os.umask(0o077)
    try:
        args = parse_args()
        command = {"scan": scan, "draft": draft, "import": import_cases}[args.command]
        print(json_bytes(command(args, Project(args))).decode("utf-8"), end="")
    except (
        OSError,
        ValueError,
        RuntimeError,
        RecursionError,
        subprocess.TimeoutExpired,
    ) as error:
        # JSON parse errors may contain input; never echo session or draft bytes.
        if isinstance(error, (json.JSONDecodeError, UnicodeError)):
            print("collect-evolve-cases: invalid UTF-8 or JSON input", file=sys.stderr)
        else:
            print(f"collect-evolve-cases: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
