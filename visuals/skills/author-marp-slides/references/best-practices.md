# Marp Authoring Best Practices

## Content

- One message per slide.
- Prefer 3-5 bullets; split dense slides.
- Use concrete nouns and verbs in headings.
- Keep code and tables readable at presentation size.

## Design

- Reuse one palette, one spacing unit, and one heading hierarchy.
- Prefer background image syntax for diagrams and photos when layout requires it; give meaningful backgrounds an adjacent semantic equivalent.
- Measure actual text/background contrast and inspect the exported deck on the target projector before claiming venue suitability.
- Keep diagrams, tables, and text aligned to a simple grid.

## HTML Policy

Use Markdown first. Use inline HTML only when Marp Markdown cannot express the layout and the target renderer is known to allow HTML.

## Accessibility

- Maintain text contrast of at least WCAG AA.
- Do not encode meaning by color alone.
- Avoid tiny captions and overcrowded diagrams.
- Avoid emoji when predictable rendering matters.

## Handoff Check

Resolve `scripts/check_marpit_structure.sh` against the `author-marp-slides` skill directory and run its limited delimiter/directive precheck:

```shell
AUTHORING_MARP_SLIDES_SKILL_DIR="/absolute/path/to/author-marp-slides"
bash "$AUTHORING_MARP_SLIDES_SKILL_DIR/scripts/check_marpit_structure.sh" deck.md
```

This does not parse YAML or Marp syntax. Follow with the actual preview/export workflow and inspect at least the title, densest content slide, every SVG/background image, and the exported accessibility tree when meaningful visuals are present.
