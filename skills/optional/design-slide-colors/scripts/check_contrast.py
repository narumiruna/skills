# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Check color contrast ratios for WCAG compliance."""

import re
import sys


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


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate relative luminance of RGB color."""

    def adjust(val):
        val = val / 255.0
        return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate contrast ratio between two hex colors."""
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))

    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)

    return (lighter + 0.05) / (darker + 0.05)


def check_wcag(ratio: float) -> dict:
    """Check WCAG compliance levels."""
    return {
        "AA_normal": ratio >= 4.5,
        "AA_large": ratio >= 3.0,
        "AAA_normal": ratio >= 7.0,
        "AAA_large": ratio >= 4.5,
        "ratio": ratio,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: check_contrast.py <foreground-hex> <background-hex>")
        print("\nExample: check_contrast.py '#D4D4D4' '#1E1E1E'")
        print("\nWCAG Standards:")
        print("  AA  - Normal text: 4.5:1, Large text: 3.0:1")
        print("  AAA - Normal text: 7.0:1, Large text: 4.5:1")
        sys.exit(1)

    fg = sys.argv[1]
    bg = sys.argv[2]

    try:
        ratio = contrast_ratio(fg, bg)
        wcag = check_wcag(ratio)

        print(f"\nColors: {fg} on {bg}")
        print(f"Contrast ratio: {ratio:.2f}:1\n")
        print(
            f"WCAG AA (normal text):  {'✅ Pass' if wcag['AA_normal'] else '❌ Fail'} (≥4.5:1)"
        )
        print(
            f"WCAG AA (large text):   {'✅ Pass' if wcag['AA_large'] else '❌ Fail'} (≥3.0:1)"
        )
        print(
            f"WCAG AAA (normal text): {'✅ Pass' if wcag['AAA_normal'] else '❌ Fail'} (≥7.0:1)"
        )
        print(
            f"WCAG AAA (large text):  {'✅ Pass' if wcag['AAA_large'] else '❌ Fail'} (≥4.5:1)"
        )

        # Exit with error if doesn't meet AA normal text
        if not wcag["AA_normal"]:
            print(
                "\n⚠️  Warning: Does not meet minimum WCAG AA standard for normal text"
            )
            sys.exit(1)

    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
