# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Generate slide color palettes from brand colors or strategies."""

import re
import shlex
import sys
from colorsys import hls_to_rgb, rgb_to_hls
from pathlib import Path
from typing import Any, cast

SCRIPT_PATH = Path(__file__).resolve()
CONTRAST_CHECKER_PATH = SCRIPT_PATH.with_name("check_contrast.py")


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a three-channel hexadecimal color to an RGB tuple."""
    normalized = hex_color.removeprefix("#")
    if re.fullmatch(r"[0-9A-Fa-f]{6}", normalized) is None:
        raise ValueError(
            f"Invalid hex color: {hex_color!r} (expected #RRGGBB or RRGGBB)"
        )
    r = int(normalized[0:2], 16)
    g = int(normalized[2:4], 16)
    b = int(normalized[4:6], 16)
    return (r, g, b)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color."""
    r, g, b = [max(0, min(255, int(x))) for x in rgb]
    return f"#{r:02x}{g:02x}{b:02x}"


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate WCAG relative luminance for an RGB color."""

    def adjust(value: int) -> float:
        channel = value / 255.0
        return (
            channel / 12.92
            if channel <= 0.03928
            else ((channel + 0.055) / 1.055) ** 2.4
        )

    red, green, blue = rgb
    return 0.2126 * adjust(red) + 0.7152 * adjust(green) + 0.0722 * adjust(blue)


def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate the WCAG contrast ratio between two hex colors."""
    luminance1 = relative_luminance(hex_to_rgb(color1))
    luminance2 = relative_luminance(hex_to_rgb(color2))
    lighter = max(luminance1, luminance2)
    darker = min(luminance1, luminance2)
    return (lighter + 0.05) / (darker + 0.05)


def adjust_lightness(hex_color: str, factor: float) -> str:
    """Adjust color lightness. Factor > 1 lightens, < 1 darkens."""
    r, g, b = hex_to_rgb(hex_color)
    h, lightness, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    lightness = max(0, min(1, lightness * factor))
    r, g, b = hls_to_rgb(h, lightness, s)
    return rgb_to_hex((int(r * 255), int(g * 255), int(b * 255)))


def adjust_saturation(hex_color: str, factor: float) -> str:
    """Adjust color saturation. Factor > 1 more saturated, < 1 less saturated."""
    r, g, b = hex_to_rgb(hex_color)
    h, lightness, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    s = max(0, min(1, s * factor))
    r, g, b = hls_to_rgb(h, lightness, s)
    return rgb_to_hex((int(r * 255), int(g * 255), int(b * 255)))


def generate_palette_from_brand(
    brand_color: str, style: str = "light"
) -> dict[str, str]:
    """
    Generate 7-role color palette from single brand color.

    Args:
        brand_color: Hex color of brand (used as Primary)
        style: "light" or "dark" background style

    Returns:
        Dictionary with 7 color roles
    """
    if style not in {"light", "dark"}:
        raise ValueError("Style must be 'light' or 'dark'")
    brand_color = rgb_to_hex(hex_to_rgb(brand_color)).upper()

    if style == "dark":
        return {
            "Background": "#1E1E1E",
            "Surface": "#252526",
            "Primary": brand_color,
            "Secondary": adjust_saturation(adjust_lightness(brand_color, 1.2), 0.8),
            "Accent": adjust_lightness(brand_color, 1.4),
            "Text Primary": "#D4D4D4",
            "Text Secondary": "#858585",
        }
    else:  # light
        return {
            "Background": "#FAFAFA",
            "Surface": "#FFFFFF",
            "Primary": brand_color,
            "Secondary": adjust_lightness(brand_color, 1.3),
            "Accent": adjust_saturation(brand_color, 1.2),
            "Text Primary": "#2C2C2C",
            "Text Secondary": "#666666",
        }


SVG_PALETTES = {
    "default": {
        "name": "Default Palette (Neutral + Blue)",
        "best_for": "Technical documentation, professional presentations",
        "colors": {
            "Dark": "#111827",
            "Mid": "#6B7280",
            "Light": "#E5E7EB",
            "Accent": "#2563EB",
            "Success": "#10B981",
            "Warning": "#F59E0B",
            "Error": "#EF4444",
        },
        "usage": [
            "Dark: Primary text, strokes, borders",
            "Mid: Secondary text, inactive elements",
            "Light: Backgrounds, fills",
            "Accent: Highlights, active states, CTAs",
        ],
    },
    "corporate": {
        "name": "Corporate Professional",
        "best_for": "Business presentations, formal reports",
        "colors": {
            "Primary": "#1E3A8A",
            "Secondary": "#0F766E",
            "Neutral": "#374151",
            "Light": "#F3F4F6",
            "Accent": "#DC2626",
        },
        "example": '<rect fill="#F3F4F6" stroke="#1E3A8A" stroke-width="4"/>\n<text fill="#374151">Label</text>',
    },
    "creative": {
        "name": "Creative & Modern",
        "best_for": "Marketing, creative pitches, modern products",
        "colors": {
            "Primary": "#7C3AED",
            "Secondary": "#EC4899",
            "Tertiary": "#F59E0B",
            "Dark": "#1F2937",
            "Light": "#FEF3C7",
        },
        "example": '<linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">\n  <stop offset="0%" style="stop-color:#7C3AED"/>\n  <stop offset="100%" style="stop-color:#EC4899"/>\n</linearGradient>\n<rect fill="url(#gradient1)"/>',
    },
    "monochrome": {
        "name": "Minimal Monochrome",
        "best_for": "Elegant, distraction-free presentations",
        "colors": {
            "Black": "#000000",
            "DarkGray": "#404040",
            "MidGray": "#808080",
            "LightGray": "#E0E0E0",
            "White": "#FFFFFF",
        },
        "example": '<rect fill="#FFFFFF" stroke="#000000" stroke-width="4"/>\n<text fill="#404040">Subtle label</text>',
    },
    "data-viz": {
        "name": "Data Visualization",
        "best_for": "Charts, graphs, multi-category comparisons",
        "colors": {
            "Category1": "#2563EB",
            "Category2": "#10B981",
            "Category3": "#F59E0B",
            "Category4": "#EF4444",
            "Category5": "#8B5CF6",
            "Category6": "#06B6D4",
            "Neutral": "#6B7280",
        },
        "notes": "Each category gets a distinct color for clarity",
    },
    "academic": {
        "name": "Academic / Scientific",
        "best_for": "Research presentations, educational content",
        "colors": {
            "Primary": "#1E40AF",
            "Secondary": "#059669",
            "Neutral": "#374151",
            "Light": "#F9FAFB",
            "Highlight": "#FBBF24",
        },
    },
    "dark-mode": {
        "name": "Dark Mode",
        "best_for": "Night presentations, developer content",
        "colors": {
            "Background": "#0F172A",
            "Surface": "#1E293B",
            "Primary": "#60A5FA",
            "Secondary": "#34D399",
            "Text": "#F1F5F9",
            "Muted": "#64748B",
        },
        "example": '<svg viewBox="0 0 1920 1080" width="1920" height="1080">\n  <rect width="1920" height="1080" fill="#0F172A"/>\n  <rect x="240" y="320" width="400" height="200" rx="16" fill="#1E293B" stroke="#60A5FA" stroke-width="4"/>\n  <text fill="#F1F5F9">Dark mode text</text>\n</svg>',
    },
    "pastel": {
        "name": "Pastel Soft",
        "best_for": "Friendly, approachable content, design presentations",
        "colors": {
            "Pink": "#FBCFE8",
            "Purple": "#DDD6FE",
            "Blue": "#BFDBFE",
            "Green": "#BBF7D0",
            "Yellow": "#FEF08A",
            "Dark": "#374151",
        },
        "example": '<rect fill="#BFDBFE" stroke="#374151" stroke-width="3"/>\n<text fill="#374151">Soft, friendly label</text>',
    },
    "high-contrast": {
        "name": "High Contrast Candidate",
        "best_for": "Starting point for diagrams that need strong color separation",
        "colors": {
            "Black": "#000000",
            "White": "#FFFFFF",
            "Yellow": "#FACC15",
            "Cyan": "#22D3EE",
            "Magenta": "#F472B6",
        },
        "notes": "Calculate each actual pairing and test the exported artifact in its target environment",
    },
}


PALETTE_METADATA = {
    "code-blue": {
        "name": "Code-Focused Blue",
        "category": "Dark Technical",
        "best_for": "Code-heavy presentations, technical demos, system architecture",
        "notes": "Inspired by VS Code theme; familiar to developers",
    },
    "terminal-dark": {
        "name": "Terminal Dark",
        "category": "Dark Technical",
        "best_for": "Candidate for terminal, CLI, and DevOps presentations",
        "notes": "Verify every assigned pairing and the exported deck on the target projector",
    },
    "midnight-professional": {
        "name": "Midnight Professional",
        "category": "Dark Technical",
        "best_for": "Professional technical presentations with a softer feel",
        "notes": "Less harsh than pure black backgrounds",
    },
    "clean-corporate": {
        "name": "Clean Corporate",
        "category": "Light Professional",
        "best_for": "Business presentations, documentation, formal settings",
        "notes": "Conservative and widely acceptable",
    },
    "modern-minimal": {
        "name": "Modern Minimal",
        "category": "Light Professional",
        "best_for": "Modern tech companies, product presentations, startups",
        "notes": "Material Design inspired; clean and modern",
    },
    "warm-professional": {
        "name": "Warm Professional",
        "category": "Light Professional",
        "best_for": "Creative presentations, design reviews, brand-focused decks",
        "notes": "Warm palette for approachable, friendly tone",
    },
    "minimal-teal": {
        "name": "Minimal with Teal Focus",
        "category": "Accent-Driven",
        "best_for": "Story-driven presentations, keynotes, single-message slides",
        "notes": "Minimal design; let content breathe; use accent sparingly (5-10% of elements)",
    },
    "grayscale-red": {
        "name": "Gray Scale with Red Accent",
        "category": "Accent-Driven",
        "best_for": "High-impact messages, problem-solution narratives, urgent topics",
        "notes": "Red accent should be reserved for 1-2 key elements per slide",
    },
    "data-viz": {
        "name": "Data Visualization Candidate (Categorical)",
        "category": "Specialized",
        "best_for": "Starting point for charts, graphs, and multi-category data",
        "notes": "Verify series distinguishability with target charts, labels, and color-vision simulation",
    },
    "accessibility": {
        "name": "High Contrast Candidate",
        "category": "Specialized",
        "best_for": "Starting point for slides with strong contrast requirements",
        "notes": "Validate each actual pairing, noncolor cue, export, and assistive path before use",
    },
}


def generate_preset_palette(preset: str) -> dict[str, str]:
    """Generate preset palette by name."""
    presets = {
        "code-blue": {
            "Background": "#1E1E1E",
            "Surface": "#252526",
            "Primary": "#569CD6",
            "Secondary": "#4EC9B0",
            "Accent": "#F4BF75",
            "Text Primary": "#D4D4D4",
            "Text Secondary": "#858585",
        },
        "terminal-dark": {
            "Background": "#0C0C0C",
            "Surface": "#1A1A1A",
            "Primary": "#61AFEF",
            "Secondary": "#98C379",
            "Accent": "#E06C75",
            "Text Primary": "#ABB2BF",
            "Text Secondary": "#5C6370",
        },
        "midnight-professional": {
            "Background": "#1B2B34",
            "Surface": "#253340",
            "Primary": "#6699CC",
            "Secondary": "#5FB3B3",
            "Accent": "#FAC863",
            "Text Primary": "#CDD3DE",
            "Text Secondary": "#A7ADBA",
        },
        "clean-corporate": {
            "Background": "#FAFAFA",
            "Surface": "#FFFFFF",
            "Primary": "#2E75B6",
            "Secondary": "#5B9BD5",
            "Accent": "#F39C12",
            "Text Primary": "#2C2C2C",
            "Text Secondary": "#666666",
        },
        "modern-minimal": {
            "Background": "#F5F5F5",
            "Surface": "#FFFFFF",
            "Primary": "#1976D2",
            "Secondary": "#757575",
            "Accent": "#FF6F00",
            "Text Primary": "#212121",
            "Text Secondary": "#616161",
        },
        "warm-professional": {
            "Background": "#FFF8F0",
            "Surface": "#FFFFFF",
            "Primary": "#D84315",
            "Secondary": "#6D4C41",
            "Accent": "#F57C00",
            "Text Primary": "#3E2723",
            "Text Secondary": "#795548",
        },
        "minimal-teal": {
            "Background": "#FFFFFF",
            "Surface": "#F8F9FA",
            "Primary": "#343A40",
            "Secondary": "#6C757D",
            "Accent": "#20C997",
            "Text Primary": "#212529",
            "Text Secondary": "#6C757D",
        },
        "grayscale-red": {
            "Background": "#F0F0F0",
            "Surface": "#FFFFFF",
            "Primary": "#2F2F2F",
            "Secondary": "#5F5F5F",
            "Accent": "#E53935",
            "Text Primary": "#1A1A1A",
            "Text Secondary": "#757575",
        },
        "data-viz": {
            "Background": "#FFFFFF",
            "Surface": "#F8F9FA",
            "Category 1": "#4E79A7",
            "Category 2": "#F28E2B",
            "Category 3": "#E15759",
            "Category 4": "#76B7B2",
            "Category 5": "#59A14F",
            "Category 6": "#EDC948",
            "Text Primary": "#2C2C2C",
            "Text Secondary": "#666666",
        },
        "accessibility": {
            "Background": "#FFFFFF",
            "Surface": "#F5F5F5",
            "Primary": "#0052CC",
            "Secondary": "#5E6C84",
            "Accent": "#FF991F",
            "Text Primary": "#000000",
            "Text Secondary": "#42526E",
        },
    }

    if preset not in presets:
        raise ValueError(f"Unknown preset: {preset}")

    return presets[preset]


def format_palette_markdown(palette: dict[str, str], preset_name: str = "") -> str:
    """Format palette as markdown output with metadata."""
    output = []

    # Add palette name and metadata if it's a preset
    if preset_name and preset_name in PALETTE_METADATA:
        meta = PALETTE_METADATA[preset_name]
        output.append(f"## {meta['name']}\n")
        output.append(f"**Category:** {meta['category']}")
        output.append(f"**Best for:** {meta['best_for']}")
        output.append(f"**Notes:** {meta['notes']}")
    else:
        output.append("## Color Palette")

    background = palette.get("Background")
    if background:
        ratios = [
            f"{role}/Background = {contrast_ratio(color, background):.2f}:1"
            for role in (
                "Text Primary",
                "Text Secondary",
                "Primary",
                "Secondary",
                "Accent",
            )
            if (color := palette.get(role)) is not None
        ]
        output.append(f"**Calculated contrast:** {', '.join(ratios)}\n")
    else:
        output.append("")

    # Display colors
    for role, color in palette.items():
        output.append(f"- **{role}:** `{color.upper()}`")

    output.append("\n## Usage Guidelines\n")
    output.append("Apply this palette to slides and SVGs consistently:\n")
    output.append(
        "- **Slides**: Use Background for slide backgrounds, Primary for titles"
    )
    output.append(
        "- **SVG**: Use Primary for main elements, Secondary for supporting elements"
    )

    # Only show text usage guideline if palette has text colors
    if "Text Primary" in palette:
        output.append(
            "- **Text**: Use Text Primary for body, Text Secondary for captions"
        )

    # Add validation section only for palettes with standard structure
    if "Text Primary" in palette and "Background" in palette:
        output.append("\n## Validation\n")
        output.append("Check contrast ratios:")
        output.append(
            f"```bash\nuv run {shlex.quote(str(CONTRAST_CHECKER_PATH))} "
            f"'{palette['Text Primary']}' '{palette['Background']}'\n```"
        )

    return "\n".join(output)


def list_palettes() -> str:
    """List all available palettes grouped by category."""
    output = ["# Available Color Palettes\n"]

    # Group palettes by category
    by_category = {}
    for preset_id, meta in PALETTE_METADATA.items():
        category = meta["category"]
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((preset_id, meta))

    # Display by category
    for category in [
        "Dark Technical",
        "Light Professional",
        "Accent-Driven",
        "Specialized",
    ]:
        if category in by_category:
            output.append(f"## {category}\n")
            for preset_id, meta in by_category[category]:
                output.append(f"**{preset_id}** - {meta['name']}")
                output.append(f"  {meta['best_for']}\n")

    output.append("\n## Usage\n")
    output.append("Show details for a specific palette:")
    output.append("```bash")
    output.append(f"uv run {shlex.quote(str(SCRIPT_PATH))} show <palette-name>")
    output.append("```\n")
    output.append("Example:")
    output.append("```bash")
    output.append(f"uv run {shlex.quote(str(SCRIPT_PATH))} show code-blue")
    output.append("```")

    return "\n".join(output)


def list_svg_palettes() -> str:
    """List all available SVG palettes."""
    output = ["# Available SVG Color Palettes\n"]
    output.append("Quick color schemes for rapid SVG illustration creation.\n")

    for palette_id, meta in SVG_PALETTES.items():
        output.append(f"**{palette_id}** - {meta['name']}")
        output.append(f"  {meta['best_for']}\n")

    output.append("\n## Usage\n")
    output.append("Show details for a specific SVG palette:")
    output.append("```bash")
    output.append(f"uv run {shlex.quote(str(SCRIPT_PATH))} svg-show <palette-name>")
    output.append("```\n")
    output.append("Example:")
    output.append("```bash")
    output.append(f"uv run {shlex.quote(str(SCRIPT_PATH))} svg-show default")
    output.append(f"uv run {shlex.quote(str(SCRIPT_PATH))} svg-show creative")
    output.append("```")

    return "\n".join(output)


def format_svg_palette(palette_id: str) -> str:
    """Format SVG palette as markdown output."""
    if palette_id not in SVG_PALETTES:
        raise ValueError(f"Unknown SVG palette: {palette_id}")

    palette: dict[str, Any] = SVG_PALETTES[palette_id]
    output = []

    # Header
    output.append(f"## {palette['name']}\n")
    output.append(f"**Best for:** {palette['best_for']}\n")

    # Colors
    output.append("### Colors\n")
    output.append("```")
    colors = cast(dict[str, str], palette["colors"])
    for role, color in colors.items():
        output.append(f"{role:12s} {color}")
    output.append("```\n")

    # Usage notes if present
    if "usage" in palette:
        output.append("**Usage:**")
        for usage_line in palette["usage"]:
            output.append(f"- {usage_line}")
        output.append("")

    # Example code if present
    if "example" in palette:
        output.append("### Example\n")
        output.append("```xml")
        output.append(palette["example"])
        output.append("```\n")

    # Additional notes if present
    if "notes" in palette:
        output.append(f"**Note:** {palette['notes']}\n")

    return "\n".join(output)


def format_palette_css(palette: dict[str, str]) -> str:
    """Format palette as CSS variables."""
    output = [":root {"]
    for role, color in palette.items():
        var_name = role.lower().replace(" ", "-")
        output.append(f"  --color-{var_name}: {color.upper()};")
    output.append("}")
    return "\n".join(output)


def print_usage() -> None:
    """Print CLI usage."""
    print(
        """Generate and manage color palettes for slides and SVG illustrations.

Usage:
  generate_palette.py list
  generate_palette.py show <palette-name>
  generate_palette.py brand <hex-color> [light|dark]
  generate_palette.py svg-list
  generate_palette.py svg-show <palette-name>
""".strip()
    )


def require_arg_count(args: list[str], count: int, usage: str) -> None:
    """Raise a concise error when a command gets the wrong number of args."""
    if len(args) != count:
        raise ValueError(usage)


def main(argv: list[str] | None = None) -> int:
    """Run the palette CLI."""
    args = sys.argv[1:] if argv is None else argv
    if not args or args[0] in {"-h", "--help"}:
        print_usage()
        return 0

    command, *rest = args
    try:
        if command == "list":
            require_arg_count(rest, 0, "Usage: generate_palette.py list")
            print(list_palettes())
        elif command == "show":
            require_arg_count(rest, 1, "Usage: generate_palette.py show <palette-name>")
            print(format_palette_markdown(generate_preset_palette(rest[0]), rest[0]))
        elif command == "brand":
            if len(rest) not in {1, 2}:
                raise ValueError(
                    "Usage: generate_palette.py brand <hex-color> [light|dark]"
                )
            style = rest[1] if len(rest) == 2 else "light"
            if style not in {"light", "dark"}:
                raise ValueError("Style must be 'light' or 'dark'")
            print(format_palette_markdown(generate_palette_from_brand(rest[0], style)))
        elif command == "svg-list":
            require_arg_count(rest, 0, "Usage: generate_palette.py svg-list")
            print(list_svg_palettes())
        elif command == "svg-show":
            require_arg_count(
                rest, 1, "Usage: generate_palette.py svg-show <palette-name>"
            )
            print(format_svg_palette(rest[0]))
        else:
            raise ValueError(f"Unknown command: {command}")
    except ValueError as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
