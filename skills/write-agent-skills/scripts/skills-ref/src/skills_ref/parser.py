# Local modifications: add lint metadata and fix frontmatter parsing and reads.
# /// script
# requires-python = ">=3.11"
# dependencies = ["strictyaml>=1.7.3"]
# ///
"""YAML frontmatter parsing for SKILL.md files."""

import re
from pathlib import Path
from typing import Optional

import strictyaml

from .errors import ParseError, ValidationError
from .models import SkillProperties

_FRONTMATTER_BOUNDARY = re.compile(r"^---[ \t]*\r?$", re.MULTILINE)


def find_skill_md(skill_dir: Path) -> Optional[Path]:
    """Find the SKILL.md file in a skill directory.

    Prefers SKILL.md (uppercase) but accepts skill.md (lowercase).

    Args:
        skill_dir: Path to the skill directory

    Returns:
        Path to the SKILL.md file, or None if not found
    """
    for name in ("SKILL.md", "skill.md"):
        path = skill_dir / name
        if path.exists():
            return path
    return None


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from SKILL.md content.

    Args:
        content: Raw content of SKILL.md file

    Returns:
        Tuple of (metadata dict, markdown body)

    Raises:
        ParseError: If frontmatter is missing or invalid
    """
    opening = _FRONTMATTER_BOUNDARY.match(content)
    if opening is None:
        raise ParseError("SKILL.md must start with YAML frontmatter (---)")

    closing = _FRONTMATTER_BOUNDARY.search(content, opening.end())
    if closing is None:
        raise ParseError("SKILL.md frontmatter not properly closed with ---")

    frontmatter_str = content[opening.end() : closing.start()]
    body = content[closing.end() :].strip()

    try:
        parsed = strictyaml.load(frontmatter_str)
        metadata = parsed.data
    except strictyaml.YAMLError as e:
        raise ParseError(f"Invalid YAML in frontmatter: {e}")

    if not isinstance(metadata, dict):
        raise ParseError("SKILL.md frontmatter must be a YAML mapping")

    if "metadata" in metadata:
        entries = metadata["metadata"]
        if not isinstance(entries, dict) or not all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in entries.items()
        ):
            raise ParseError("Field 'metadata' must map strings to strings")

    if "allowed-tools" in metadata and not isinstance(metadata["allowed-tools"], str):
        raise ParseError("Field 'allowed-tools' must be a string")

    return metadata, body


def read_frontmatter(skill_md: Path) -> tuple[dict, str]:
    """Read and parse frontmatter from a UTF-8 skill file."""
    try:
        content = skill_md.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ParseError(f"Cannot read {skill_md} as UTF-8: {error}") from error
    return parse_frontmatter(content)


def read_properties(skill_dir: Path) -> SkillProperties:
    """Read skill properties from SKILL.md frontmatter.

    This function parses the frontmatter and returns properties.
    It does NOT perform full validation. Use validate() for that.

    Args:
        skill_dir: Path to the skill directory

    Returns:
        SkillProperties with parsed metadata

    Raises:
        ParseError: If SKILL.md is missing or has invalid YAML
        ValidationError: If required fields (name, description) are missing
    """
    skill_dir = Path(skill_dir)
    skill_md = find_skill_md(skill_dir)

    if skill_md is None:
        raise ParseError(f"SKILL.md not found in {skill_dir}")

    metadata, _ = read_frontmatter(skill_md)

    if "name" not in metadata:
        raise ValidationError("Missing required field in frontmatter: name")
    if "description" not in metadata:
        raise ValidationError("Missing required field in frontmatter: description")

    name = metadata["name"]
    description = metadata["description"]

    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Field 'name' must be a non-empty string")
    if not isinstance(description, str) or not description.strip():
        raise ValidationError("Field 'description' must be a non-empty string")

    return SkillProperties(
        name=name.strip(),
        description=description.strip(),
        license=metadata.get("license"),
        compatibility=metadata.get("compatibility"),
        allowed_tools=metadata.get("allowed-tools"),
        metadata=metadata.get("metadata", {}),
    )
