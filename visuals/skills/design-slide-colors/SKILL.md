---
name: design-slide-colors
description: Design, adapt, generate, or validate slide color systems and semantic palettes, including brand-color integration, usage roles, contrast evidence, and presentation-environment caveats.
---

# Slide Color Design

Use a seven-role semantic system so color choices remain consistent across slides and visuals.

| Need | Read or use |
| --- | --- |
| End-to-end palette workflow | `references/color-design/workflow.md` |
| Strategy tradeoffs | `references/color-design/strategies.md` |
| Adaptable handoff format | `references/color-design/output-template.md` |
| Candidate palettes | `references/color-palettes.md` |
| Generated starting point | `scripts/generate_palette.py` |
| Contrast calculation | `scripts/check_contrast.py` |

## Workflow

1. Identify audience, content density, delivery environment, existing theme, and brand constraints. State only assumptions that affect the palette.
2. Choose or adapt a strategy and define Background, Surface, Primary, Secondary, Accent, Text Primary, and Text Secondary roles. Roles may share a color when hierarchy remains clear; add semantic colors only when needed.
3. Give each color a purpose and usage rule. Preserve brand colors while adjusting surrounding roles to meet readability needs.
4. Calculate contrast for every text/background pairing that will actually be used. Record ratios and applicable thresholds rather than claiming general accessibility from one pair.
5. Apply the palette to representative title, content, code/data, and visual slides when available; check hierarchy and color-meaning consistency.
6. Return the palette and usage rules first, followed by measured evidence and untested conditions. Leave projector, print, recording, and venue checks explicitly open unless performed.

Do not open authoring or SVG references for a palette-only request. Do not mark a validation item complete without direct evidence.
