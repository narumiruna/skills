# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "packaging>=26.3",
# ]
# ///
"""Check Python inline metadata and executable headers without running scripts.

Run `prek run lint-python-scripts -a` to check every tracked .py file, including
helpers and deprecated scripts, or pass filenames directly to this script.
Dependency declarations are validated, not inferred from imports.
"""

import argparse
import pathlib
import re
import sys
import tomllib

from packaging import requirements
from packaging import specifiers

UV_SHEBANG = "#!/usr/bin/env -S uv run --script"
# Canonical pattern from the PyPA inline script metadata specification.
METADATA_PATTERN = re.compile(
    r"(?m)^# /// (?P<type>[a-zA-Z0-9-]+)$\s"
    r"(?P<content>(^#(| .*)$\s)+)^# ///$"
)


def check_metadata(source: str) -> list[str]:
    """Return errors for missing, duplicate, or invalid script metadata."""
    blocks = [
        match
        for match in METADATA_PATTERN.finditer(source)
        if match.group("type") == "script"
    ]
    if len(blocks) != 1:
        return ["expected exactly one complete '# /// script' metadata block"]

    content = "".join(
        line[2:] if line.startswith("# ") else line[1:]
        for line in blocks[0].group("content").splitlines(keepends=True)
    )
    try:
        metadata = tomllib.loads(content)
    except tomllib.TOMLDecodeError as error:
        return [f"invalid script metadata TOML: {error}"]

    errors = []
    dependencies = metadata.get("dependencies")
    if not isinstance(dependencies, list):
        errors.append("dependencies must be an array; use [] when none are needed")
    else:
        for dependency in dependencies:
            if not isinstance(dependency, str):
                errors.append("each dependency must be a PEP 508 string")
                continue
            try:
                requirements.Requirement(dependency)
            except requirements.InvalidRequirement as error:
                errors.append(f"invalid dependency {dependency!r}: {error}")

    if "requires-python" in metadata:
        version = metadata["requires-python"]
        if not isinstance(version, str):
            errors.append("requires-python must be a version specifier string")
        else:
            try:
                specifiers.SpecifierSet(version)
            except specifiers.InvalidSpecifier as error:
                errors.append(f"invalid requires-python: {error}")
    return errors


def check_file(path: pathlib.Path) -> list[str]:
    """Return metadata and executable-header errors for one UTF-8 Python file."""
    source = path.read_text(encoding="utf-8")
    errors = check_metadata(source)
    first_line = source.partition("\n")[0]
    executable = bool(path.stat().st_mode & 0o111)
    if first_line.startswith("#!"):
        if first_line != UV_SHEBANG:
            errors.append(f"the shebang must be {UV_SHEBANG!r}")
        if not executable:
            errors.append("a script with a shebang must have an executable bit set")
    elif executable:
        errors.append(f"an executable Python file must start with {UV_SHEBANG!r}")
    return errors


def main() -> int:
    """Check supplied filenames and return nonzero if any file fails."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=pathlib.Path)
    args = parser.parse_args()

    status = 0
    for path in args.files:
        try:
            errors = check_file(path)
        except (OSError, UnicodeError) as error:
            errors = [f"cannot read script: {error}"]
        for error in errors:
            print(f"{path}: {error}", file=sys.stderr)
            status = 1
    if not status:
        print(f"Checked {len(args.files)} Python file(s).")
    return status


if __name__ == "__main__":
    sys.exit(main())
