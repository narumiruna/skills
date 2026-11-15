#!/usr/bin/env python3
"""Replace Cursor directory references in skill text files.

Run `prek run normalize-skill-paths -a` to scan all tracked active skill text
files, or pass filenames to this script. File contents are changed in place;
directories are not renamed. Exit with status 1 after fixes, or 0 if unchanged.
"""

import argparse
import pathlib
import sys

OLD_PATH = b".cursor/"
NEW_PATH = b".agents/"


def fix_file(path: pathlib.Path) -> bool:
    """Replace path references in a UTF-8 file and return whether it changed."""
    if path.is_symlink() or not path.is_file():
        return False

    content = path.read_bytes()
    if b"\0" in content:
        return False
    try:
        content.decode("utf-8")
    except UnicodeDecodeError:
        return False

    updated = content.replace(OLD_PATH, NEW_PATH)
    if updated == content:
        return False

    path.write_bytes(updated)
    print(f"{path}: replaced {content.count(OLD_PATH)} path reference(s)")
    return True


def main() -> int:
    """Process all supplied files and return the hook exit status."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=pathlib.Path)
    args = parser.parse_args()

    status = 0
    for path in args.files:
        try:
            if fix_file(path):
                status = 1
        except OSError as error:
            print(f"{path}: {error}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
