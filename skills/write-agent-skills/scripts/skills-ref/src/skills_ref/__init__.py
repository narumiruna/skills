# Local modification: add inline metadata for this repository's lint gate.
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Reference library for Agent Skills."""

from .errors import ParseError, SkillError, ValidationError
from .models import SkillProperties
from .parser import find_skill_md, read_properties
from .prompt import to_prompt
from .validator import validate

__all__ = [
    "SkillError",
    "ParseError",
    "ValidationError",
    "SkillProperties",
    "find_skill_md",
    "validate",
    "read_properties",
    "to_prompt",
]

__version__ = "0.1.0"
