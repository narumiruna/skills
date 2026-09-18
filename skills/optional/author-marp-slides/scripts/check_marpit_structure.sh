#!/bin/bash
# Check basic Marpit Markdown structure without parsing YAML or rendering slides.

set -e

if [ $# -ne 1 ]; then
    echo "Usage: check_marpit_structure.sh <file.md>"
    echo ""
    echo "Checks only:"
    echo "  - Frontmatter opening and closing delimiters"
    echo "  - A literal 'marp: true' directive in frontmatter"
    echo "  - Structural slide-separator count"
    echo ""
    echo "This does not parse YAML or validate rendered Marp output."
    exit 1
fi

FILE="$1"
case "$FILE" in
    /*) ;;
    *) FILE="./$FILE" ;;
esac

if [ ! -f "$FILE" ]; then
    echo "❌ File not found: $FILE"
    exit 1
fi

ERRORS=0

# Check frontmatter opening, accepting CRLF input.
FIRST_LINE=$(head -n 1 -- "$FILE")
FIRST_LINE=${FIRST_LINE%$'\r'}
if [ "$FIRST_LINE" != "---" ]; then
    echo "❌ Missing frontmatter opening (---) on line 1"
    ERRORS=$((ERRORS + 1))
fi

# Locate the frontmatter closing delimiter.
FRONTMATTER_END=$(awk '{ sub(/\r$/, "") } NR > 1 && $0 == "---" { print NR; exit }' "$FILE")
if [ -z "$FRONTMATTER_END" ]; then
    echo "❌ Missing frontmatter closing delimiter (---)"
    ERRORS=$((ERRORS + 1))
else
    # Check marp: true inside frontmatter only.
    if ! awk -v end="$FRONTMATTER_END" '{ sub(/\r$/, "") } NR > 1 && NR < end' "$FILE" | grep -Eq '^marp:[[:space:]]*[Tt][Rr][Uu][Ee]([[:space:]]*#.*)?[[:space:]]*$'; then
        echo "❌ Missing 'marp: true' in frontmatter"
        ERRORS=$((ERRORS + 1))
    fi
fi

# Count separators and slides, accepting CRLF input and avoiding negative counts.
SEPARATOR_COUNT=$(awk '{ sub(/\r$/, "") } $0 == "---" { count++ } END { print count + 0 }' "$FILE")
if [ "$SEPARATOR_COUNT" -gt 0 ]; then
    SLIDE_COUNT=$((SEPARATOR_COUNT - 1))
else
    SLIDE_COUNT=0
fi

if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Structural precheck passed"
    echo "   File: $FILE"
    echo "   Slides: $SLIDE_COUNT"
    echo "   Note: YAML and rendered Marp output were not validated"
    exit 0
fi

echo ""
echo "❌ Found $ERRORS structural issue(s)"
exit 1
