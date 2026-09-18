# Slide Palette Reference

Use the bundled generator as the source of truth for available palette values. Resolve the skill directory and invoke the script by absolute path:

```bash
uv run "$SKILL_DIR/scripts/generate_palette.py" list
uv run "$SKILL_DIR/scripts/generate_palette.py" show <palette-name>
```

Current categories include dark technical, light professional, accent-driven, data-visualization, and high-contrast starting points. Inspect `list` output rather than duplicating the complete catalog here.

## Brand Starting Points

```bash
uv run "$SKILL_DIR/scripts/generate_palette.py" brand '#2E75B6' light
uv run "$SKILL_DIR/scripts/generate_palette.py" brand '#569CD6' dark
```

Generated brand palettes are candidates, not validated brand systems. Preserve official brand values, assign them roles they can support, and calculate every text/background pairing actually used.

## SVG Candidates

```bash
uv run "$SKILL_DIR/scripts/generate_palette.py" svg-list
uv run "$SKILL_DIR/scripts/generate_palette.py" svg-show <palette-name>
```

Use the same semantic meaning across deck and SVG. Keep a single diagram to the few colors needed for hierarchy; add semantic or data-series colors only when the visual needs them.

## Selection Checks

- Background and Surface are distinguishable in the rendered artifact.
- Text Primary and Text Secondary meet the applicable contrast threshold on every assigned background.
- Primary, Secondary, and Accent have stable, documented roles.
- Essential state or series meaning has a noncolor cue.
- Venue, print, recording, and color-vision claims remain open until tested with the appropriate artifact and condition.

Run the bundled contrast checker for exact pairs:

```bash
uv run "$SKILL_DIR/scripts/check_contrast.py" '#D4D4D4' '#1E1E1E'
```
