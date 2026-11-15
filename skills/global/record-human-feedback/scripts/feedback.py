# /// script
# dependencies = []
# ///
"""Record local human feedback events and summarize their frequencies."""

import argparse
import collections
import datetime
import json
import os
import pathlib
import re
import sys
import tempfile
import uuid


CATEGORIES = {
    "tool-preference",
    "missing-action",
    "missed-context",
    "misunderstood-intent",
    "workflow-guidance",
    "incorrect-action",
    "other",
}
INPUT_FIELDS = {
    "category",
    "topic",
    "user_quote",
    "observed_behavior",
    "expected_behavior",
    "tools",
    "context",
}


def _validate_feedback(feedback):
    """Validate one event payload before it reaches the store."""
    if not isinstance(feedback, dict) or feedback.keys() != INPUT_FIELDS:
        raise ValueError(
            "Input must be an object with exactly these fields: "
            + ", ".join(sorted(INPUT_FIELDS))
        )
    for field in ("category", "topic", "user_quote"):
        value = feedback[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a nonempty string")
    if feedback["category"] not in CATEGORIES:
        raise ValueError("Unknown category: " + feedback["category"])
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", feedback["topic"]):
        raise ValueError("topic must use lowercase kebab-case")
    for field in ("observed_behavior", "expected_behavior", "context"):
        value = feedback[field]
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{field} must be a nonempty string or null")
    tools = feedback["tools"]
    if not isinstance(tools, list) or any(
        not isinstance(tool, str) or not tool.strip() for tool in tools
    ):
        raise ValueError("tools must be an array of nonempty strings")
    return {**feedback, "tools": sorted({tool.strip() for tool in tools})}


def _record(root, feedback):
    """Publish a private JSON event without replacing an existing record."""
    feedback = _validate_feedback(feedback)
    now = datetime.datetime.now(datetime.timezone.utc)
    event_id = str(uuid.uuid4())
    event = {
        **feedback,
        "schema_version": 1,
        "id": event_id,
        "recorded_at": now.isoformat(),
        "cwd": str(pathlib.Path.cwd()),
    }
    content = json.dumps(event, ensure_ascii=False, indent=2) + "\n"
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    month = root / now.strftime("%Y-%m")
    month.mkdir(mode=0o700, exist_ok=True)
    destination = month / f"{event_id}.json"
    temporary = tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=month, delete=False
    )
    try:
        with temporary:
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.link(temporary.name, destination)
    finally:
        pathlib.Path(temporary.name).unlink()
    return destination


def _rank(counts):
    """Return descending counts with deterministic alphabetical ties."""
    return [
        {"name": name, "count": count}
        for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def _summarize(root):
    """Count events without creating or changing files."""
    categories = collections.Counter()
    topics = collections.Counter()
    tools = collections.Counter()
    total = 0
    for path in sorted(root.glob("*/*.json")):
        try:
            event = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(event, dict) or event.get("schema_version") != 1:
                raise ValueError("Expected schema_version 1")
            feedback = _validate_feedback(
                {field: event[field] for field in INPUT_FIELDS}
            )
        except (KeyError, ValueError) as error:
            raise ValueError(f"Invalid feedback record: {path}: {error}") from error
        categories[feedback["category"]] += 1
        topics[feedback["topic"]] += 1
        tools.update(feedback["tools"])
        total += 1
    return {
        "total_events": total,
        "categories": _rank(categories),
        "topics": _rank(topics),
        "tools": _rank(tools),
    }


def main() -> int:
    """Run the feedback CLI, reporting failures without claiming success."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("record", "summary"),
        help="record one JSON object from stdin, or summarize saved events",
    )
    arguments = parser.parse_args()
    root = pathlib.Path.home() / ".agents" / "human-feedback"
    try:
        if arguments.command == "record":
            print(_record(root, json.load(sys.stdin)))
        else:
            print(json.dumps(_summarize(root), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        print(f"feedback: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
