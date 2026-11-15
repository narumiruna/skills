# SVG Illustration Core Rules

Create small, editable SVGs that render reliably in Marp/Marpit and HTML exports.

## Workflow

1. Choose the canvas size for the actual content.
2. Define palette, stroke width, radius, and text style once.
3. Write simple SVG: shapes, paths, text, groups.
4. Validate with `svglint file.svg` when available.
5. Embed and inspect in the target slide or doc.

## Canvas

- Set `viewBox` to the visible content bounds.
- Avoid `1920 1080` unless the graphic is a full-slide background.
- Common sizes: `1200x675` for 16:9 diagrams, `800x450` for split-column art, `200x200` for icons.
- Include `xmlns="http://www.w3.org/2000/svg"` on the root element.

## Style

- Use one palette across a deck.
- Use one stroke width, usually `3` or `4`.
- Use one corner radius, usually `12` or `16`.
- Prefer solid fills and simple shadows over complex filters.
- Avoid embedded fonts and base64 assets unless exact offline rendering is required.

## Text

- Use web-safe fallbacks: `font-family="Arial, Helvetica, sans-serif"` or monospace.
- Set explicit `font-size` and `fill`.
- Escape XML characters: `&amp;`, `&lt;`, `&gt;`.
- Avoid emoji for portable rendering.

## Minimal Template

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" aria-labelledby="title desc">
  <title id="title">Diagram title</title>
  <desc id="desc">Short description.</desc>
  <rect width="800" height="450" rx="16" fill="#F8FAFC"/>
  <g fill="#111827" font-family="Arial, Helvetica, sans-serif">
    <text x="40" y="64" font-size="32" font-weight="700">Heading</text>
  </g>
</svg>
```

## Validation

```shell
svglint path/to/file.svg
```

If `svglint` is unavailable, at least open the SVG in a browser or embed it in the deck and export once.
