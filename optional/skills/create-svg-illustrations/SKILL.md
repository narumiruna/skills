---
name: create-svg-illustrations
description: Create, revise, embed, or troubleshoot accessible SVG diagrams and illustrations for slide decks, documents, and other static artifacts, with portable sizing, layout, style, and validation guidance.
---

# SVG Illustrations

Start with `references/core-rules.md`; load only the extra detail the artifact needs.

| Need | Read or use |
| --- | --- |
| Canvas, style, text, accessibility, validation | `references/core-rules.md` |
| Reusable compositions | `references/pattern-examples.md` |
| Marp embedding | `references/embedding.md` |
| Rendering failures | `references/troubleshooting.md` |
| Known-good deck example | `assets/examples/with-diagrams.md` |

## Workflow

1. Inspect the target slide or document, required dimensions, surrounding palette, and renderer.
2. Create the smallest editable SVG that communicates the idea. Use a correct `viewBox`, explicit text styles, consistent geometry, and SVG title/description where the visual carries meaning. When embedding, also provide descriptive host-level alt text or an adjacent semantic equivalent as required by `references/embedding.md`; internal SVG metadata alone is not sufficient.
3. Keep assets portable: avoid embedded fonts, unexplained emoji, unnecessary filters, and base64 content unless the output must be self-contained.
4. Validate with `svglint` when available, then open or embed the SVG in the target artifact and inspect clipping, scaling, contrast, text, and relative paths.
5. Return the SVG artifact first, followed by validation performed and any renderer or font caveat.

Use slide-authoring or color guidance only when the request also requires it. Do not claim visual inspection when only source validation ran, and do not commit or publish the artifact unless requested.
