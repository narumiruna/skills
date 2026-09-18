# Cross-Cutting Slide Troubleshooting

## Colors Differ in the Venue

- Recheck contrast for actual foreground/background pairings.
- Export with the target renderer; transparent layers can change effective colors.
- Test the artifact on the target projector or display before claiming venue performance.
- Increase separation based on observed output rather than assuming a dark or light theme is universally safer.

## SVG Is Missing or Cropped

1. Confirm the asset path is relative to the deck file.
2. Ensure the root has `xmlns="http://www.w3.org/2000/svg"` and a `viewBox` matching visible content.
3. Run `svglint` when available.
4. Embed and export once; a standalone browser preview may not match the deck renderer.

```markdown
![Request flow diagram width:800px](diagrams/flow.svg)
```

## Exported Text Loses Contrast

Use the color skill's checker with resolved absolute script path:

```bash
uv run "$DESIGNING_SLIDE_COLORS_SKILL_DIR/scripts/check_contrast.py" \
  '#D4D4D4' '#1E1E1E'
```

Check the effective background, including transparency or images. Record the ratio and inspect the exported artifact; preview appearance alone is insufficient.

## Fonts Change

- Use portable fallback stacks and standard weights.
- Set SVG `font-family` explicitly and avoid emoji where rendering portability matters.
- Verify target fonts are available or embedded by the chosen output format.
- Inspect the densest slides after export for changed wrapping or clipping.

## Visual Style Drifts

Compare palette roles, spacing unit, type hierarchy, stroke width, radius, shadow, and Marp directives against the deck's canonical choices. Correct the inconsistent source, re-export affected slides, and report which checks were visual versus syntactic.
