# Embedding SVG in Marp/Marpit

Accessibility belongs to the host document as well as the SVG. Internal `<title>` and `<desc>` help when SVG is opened directly, but do not reliably replace host-level alternatives for external images or CSS backgrounds.

## Inline Images

Give meaningful inline images descriptive host-level alt text. Marp directives can share the alt field:

```markdown
![System architecture w:800](assets/architecture.svg)
![Company logo w:160](assets/logo.svg)
```

Use empty alt text only for a truly decorative image whose meaning is already present in nearby content.

## Background Images

Marp background syntax is useful for full-slide and split layouts, but a CSS background has no reliable image alternative:

```markdown
![bg right:45% fit](assets/architecture.svg)
```

When a background diagram carries meaning, provide an adjacent semantic equivalent in the slide's heading, body, caption, speaker notes included in the accessible deliverable, or another documented text alternative. Do not rely on the `bg`, `fit`, or sizing directives as alt text.

## Verification

- Inspect the exported accessibility tree or equivalent output, not only the source Markdown.
- Confirm meaningful inline images expose their descriptive alt text.
- Confirm every meaningful background diagram has an adjacent semantic equivalent.
- Check that decorative images do not create redundant announcements.

## Paths and Sizing

- Resolve paths relative to the slide Markdown file; do not use absolute local paths.
- Let `viewBox` define SVG content bounds and Marp control display size with `bg`, `fit`, `cover`, or `w:`.
- Keep SVG assets near the deck. Use base64 only when a self-contained artifact is required.
