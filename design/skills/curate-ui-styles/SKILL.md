---
name: curate-ui-styles
description: Create, compare, and fine-tune reusable UI style skills through a visual preference interview with three HTML previews per question. Use when the user wants to choose a UI look, save a style for future interfaces, or manage a collection of UI styles; not for one-off layout fixes.
---

# Curate UI styles

Turn visual preferences into reusable Agent Skills that tell an agent how to style a UI.
Run the interview and manage its output without changing product code, installing skills, or publishing anything unless separately requested.

## Choose the operation

- **Create:** Run a full interview for a new style.
- **Refine:** Read the selected style and ask only about the requested changes and their direct dependencies.
- **Resume:** Read the named interview draft, show its latest unanswered question or pending review, and continue without restarting.
- **Manage:** List or show saved styles, compare them on the same surface, or copy one under a new ID without changing the original.
- **Export:** Copy a selected style skill to a user-approved local destination without overwriting an existing skill.

Work in the current project unless the user supplies a different workspace.
Keep source styles in `ui-styles/ui-style-<id>/SKILL.md` by default, not in the installed meta skill.
Read the [style skill format](references/style-skill.md) before creating, refining, comparing, copying, or exporting a style.

## Set up an interview

1. Establish the product, one representative screen or flow, and any fixed brand, platform, or accessibility constraints from the request and workspace.
2. If context is missing, use a stated assumption and a representative screen, or ask one setup question if the missing context would make the choices misleading.
3. For a full interview, default to 12 visual questions (four per layer) and plan 3–5 per layer, for a total of 9–15.
4. For a refinement, skip the quota and ask only the questions needed to settle the requested change.
5. Use the [question bank](references/question-bank.md) to choose relevant axes in this order:

| Layer | User-facing label | What the user compares |
| --- | --- | --- |
| Macro | 整體（遠） | Full screens: composition, page rhythm, and visual emphasis. |
| Meso | 元件（中） | Groups of components: navigation, information surfaces, and action hierarchy. |
| Micro | 細節（近） | Close-ups: corner shapes, exact palette, type details, and borders. |

Keep a local draft at `.ui-style-interviews/<session-id>/interview.md` with a fresh session ID, or use another location requested by the user.
Record the mode, target and base style (if any), limits, ordered question IDs, current preview paths and A/B/C mappings, and explicit answers or skips.
For a refinement, also record a fingerprint or snapshot of the starting style so a resumed interview can detect outside edits.
Keep drafts separate from saved styles.

## Ask one visual question at a time

1. State the layer, progress, and the one visual decision, in the user's language.
2. Generate one self-contained HTML file with exactly three rendered options labeled A, B, and C, using the [comparison preview](assets/compare-question.html) as a starting point.
3. Keep the copy, preview frame, viewport conditions, and settled choices the same; change only properties needed to show the named axis.
4. For a refinement, include the current style as one of the options if it is viable, and make the other two clearly distinct on the same axis.
5. Open or link the preview in a client that can show it, or give its local path and a short text description of each option if HTML cannot be displayed inline.
6. Ask the user to reply in chat with A, B, or C, and wait before generating the next question.
   - Accept skip, go back, replace the variants, describe a custom choice, or finish early as reply actions, not additional visual options.
   - A preview-only click does not submit a choice to chat or save a preference.
7. Update the draft after each reply and before presenting the next question.
   - Record the actual design choice, not just the letter.
   - Record a skip as unresolved or as “keep current” for refinement.
   - When revising a question, write a new preview file and keep each letter tied to the file it was shown in.
   - If an earlier decision changes, revisit only downstream answers that depend on it and preserve the rest.

Use complete mock screens for macro choices, a realistic component group for meso choices, and close-ups in context for micro choices.
Use fictional sample content and local HTML/CSS; do not embed external assets, trackers, live actions, or raw user-supplied markup.
Check that all options stay readable, keyboard accessible when selectable, and comparable at narrow and wide widths.
Never trade contrast, focus visibility, or required UI behavior for a preference.

## Review and save

1. Combine the decisions into one representative HTML preview and summarize the confirmed rules by layer.
2. For refinement, show the before and after on the same content and name what stays unchanged.
3. Separate confirmed preferences from unresolved or unasked items; do not turn a skipped choice into a rule.
   - If no preference was confirmed, do not create an empty style or rewrite the base style.
4. Ask for confirmation of the preview, style name, and destination before creating or updating the saved style.
5. Write the style skill only after confirmation, or retain only the draft if the user pauses or cancels.
6. Check that the saved skill has valid frontmatter, uses the confirmed choices without contradictions, and can stand alone without the interview files.
7. Report the saved skill path and how to reuse it, or report the draft path and how to resume if nothing was saved.
