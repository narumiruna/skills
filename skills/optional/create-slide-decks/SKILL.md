---
name: create-slide-decks
description: Create or revise complete Marp/Marpit slide decks, coordinating narrative, slide authoring, color systems, and Mermaid or SVG visuals with rendered validation.
---

# Creating Slide Decks

Produce a coherent Marp deck, not a collection of independently styled slides. Use focused skills for detailed authoring, color, and illustration rules.

## Route the Work

| Need | Skill |
| --- | --- |
| Marp syntax, layouts, themes, templates, validation | `author-marp-slides` |
| New or adapted slide palette | `design-slide-colors` |
| Standard structured diagram with editable text source | `create-mermaid-diagrams` |
| Bespoke illustration, exact visual layout, or direct SVG | `create-svg-illustrations` |

Load only the skills needed for the requested deck. Use `references/troubleshooting-common.md` only when a cross-cutting problem appears.

## Deck Workflow

1. Inspect the brief, audience, venue or delivery format, existing deck, brand assets, content sources, and repository conventions. State only assumptions that affect design or validation.
2. Define the narrative: purpose, opening, section sequence, evidence, key takeaway, and close. Draft slide titles before styling details.
3. Establish one seven-role semantic palette when colors are not already fixed. Preserve provided brand colors and verify actual text/background pairings.
4. Author with `author-marp-slides`. Use one spacing unit and a consistent title/section/body hierarchy. Keep one primary visual anchor per section and use layout, type, spacing, and contrast before decoration.
5. Add only visuals that improve comprehension. Choose Mermaid for conventional structural diagrams and hand-authored SVG for custom composition. Keep logos, icons, and small images inline; use background syntax for full-slide or split-layout visuals.
6. Reuse palette hex values, stroke widths, corner radii, labels, and emphasis rules across slides and visuals.
7. Validate source syntax and relative asset paths, render the deck, and inspect the title, densest slide, transitions, code/data slides, and every visual slide. Check the relevant viewport, contrast, overflow, clipping, and readability constraints.
8. Return the deck and related source assets first. Then list exact checks, material caveats, and any venue, font, or renderer condition not tested.

## Constraints

- Keep Marp/Marpit Markdown as the deck source; do not silently substitute PowerPoint or Keynote.
- Prefer static, portable output. Preserve editable Mermaid or SVG source for generated visuals.
- Use repository-relative asset paths.
- Do not claim projector, print, recording, or venue validation unless it was performed.
- Deck creation does not authorize committing, publishing, or external distribution.
