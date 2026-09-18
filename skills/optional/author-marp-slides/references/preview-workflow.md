# Marp Preview Workflow

Use this when visual inspection is required.

## Preconditions

- `marp` CLI is installed.
- The deck and assets use repository-relative paths.

## Optional Human Preview

The preview server is long-running and requires a browser, so do not use it as an agent validation command.
A human can start it with:

```bash
marp -s examples/slides
```

Open the printed URL, usually:

```text
http://localhost:8080/<deck>.md
```

Jump to a slide with `#N`, for example `deck.md#5`.

## Renderer and Export Check

```bash
marp examples/slides/deck.md -o /tmp/deck.html
```

Unlike the bundled structural precheck, this invokes the Marp renderer and confirms whether it accepted the source and produced output. It does not prove strict YAML validity: malformed or ignored directives may still export. Inspect whether frontmatter directives took effect, plus the title slide, densest slide, every image/SVG slide, and the accessibility tree or equivalent when meaningful visuals are present.

## Common Fixes

- Broken image: use a relative path from the deck file.
- Cropped SVG: check the SVG `viewBox` and use `![bg fit]`.
- Low contrast: adjust the palette or image background, then re-export.
