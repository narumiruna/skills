# SVG Troubleshooting

## Broken Image

Checks:

1. Path is relative to the Markdown file.
2. SVG root includes `xmlns="http://www.w3.org/2000/svg"`.
3. XML parses with `svglint file.svg` or in a browser.

## Cropped or Tiny SVG

Cause: `viewBox` does not match content bounds.

Fix: set `viewBox="0 0 width height"` to the actual visible drawing area, then size in Marp with `![bg fit]` or `![w:...]`.

## Text Missing

Checks:

- `font-size` is explicit.
- `fill` contrasts with the background.
- Text does not rely on an unavailable embedded or system font.
- XML characters are escaped.

## Arrows Missing

Checks:

- Marker `id` exists in `<defs>`.
- Line/path uses `marker-end="url(#id)"`.
- Marker fill/stroke contrasts with the background.

## Inconsistent Visual Style

Fix by normalizing these values across all SVGs in the deck:

- palette
- stroke width
- corner radius
- font family and sizes
- shadow/filter use

## Validation

```shell
svglint path/to/file.svg
```

If `svglint` flags XML escaping, replace `&` with `&amp;`, `<` with `&lt;`, and `>` with `&gt;` inside text nodes.
