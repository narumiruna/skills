---
name: curate-ui-styles
description: Create, compare, and fine-tune reusable UI style skills through a visual preference interview with three HTML options per question and in-browser answers on one local page. Use when the user wants to choose a UI look, save a style for future interfaces, or manage a collection of UI styles; not for one-off layout fixes.
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

Run the interview in the current project unless the user supplies a different workspace.
For a new style, propose `~/.agents/skills/design/ui-style-<id>/SKILL.md` unless the user specifies another destination.
When refining an existing style, keep its current path.
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

## Serve the previews

Save question and review pages in a `previews/` subdirectory beside `interview.md`, using lowercase kebab-case filenames such as `01-page-composition.html`.
Keep drafts, saved skills, and other project content outside `previews/`; the server manages its own state files there.
On resume, if the current preview predates this layout, copy it into `previews/` and preserve its A/B/C mapping.

Use the [preview server](scripts/serve_previews.py) with `uv` and Python 3.10 or later.
Set `skill_dir` to the absolute path of this installed skill and `preview_dir` to the interview's `previews/` directory.

```bash
uv run --no-project "$skill_dir/scripts/serve_previews.py" "$preview_dir"
```

Start the command once in a managed background process, or use `nohup` with input redirected from `/dev/null` and output to a fresh log outside `previews/`, and keep the stop handle for this interview.
Check that the printed `http://127.0.0.1:<port>/` returns HTTP 200, then give it to the user once and ask them to keep that tab open.
For each completed question file, publish its exact filename as `question_html` and wait for the browser answer with a tool timeout above 180 seconds:

```bash
uv run --no-project "$skill_dir/scripts/serve_previews.py" "$preview_dir" --show-question "$question_html"
uv run --no-project "$skill_dir/scripts/serve_previews.py" "$preview_dir" --wait-for-answer "$question_html"
```

Tell the user the URL before entering the first wait, using a user-visible progress message if supported.
If the client cannot show the URL before blocking, end the turn with the URL and ask the user to say `continue` once after opening it or submitting.
Treat the returned letter like a chat answer, record it in the draft, and publish the next question without ending the turn or sending a new link.
On exit code 3, leave the tab open and tell the user they can still submit, then say `continue` in chat so you can read the pending answer for that same question.
If the user resumes a pending question, reuse its filename so a browser answer already submitted is not lost.
For a review file, use `--show-review "$review_html"` instead, which replaces the preview in the same tab without offering A/B/C.
Keep generated previews self-contained and isolated; only the viewer handles submissions.
If the browser cannot reach loopback or run the viewer, offer a direct preview URL, or a local HTML path and short descriptions, and collect the answer in chat.
Do not expose the server on the network or create a tunnel without explicit authorization.
Stop only this interview's server when the user explicitly pauses, cancels, or finishes; for a foreground run, press Ctrl+C.

## Ask one visual question at a time

1. State the layer, progress, and the one visual decision, in the user's language.
2. Generate one self-contained HTML file with exactly three rendered options labeled A, B, and C, using the [comparison preview](assets/compare-question.html) as a starting point.
3. Keep the copy, preview frame, viewport conditions, and settled choices the same; change only properties needed to show the named axis.
4. For a refinement, include the current style as one of the options if it is viable, and make the other two clearly distinct on the same axis.
5. Publish the question and wait for an explicit A/B/C submission in the browser, or use the chat fallback above.
   - Accept skip, go back, replace the variants, custom choices, or early finish in chat, not as additional visual options.
   - Show A/B/C in the generated preview as labels, not as a second set of answer controls.
6. Update the draft after each reply and before presenting the next question.
   - Record the actual design choice, not just the letter.
   - Record a skip as unresolved or as “keep current” for refinement.
   - When revising a question, write a new preview file and keep each letter tied to the file it was shown in.
   - If an earlier decision changes, revisit only downstream answers that depend on it and preserve the rest.

Use complete mock screens for macro choices, a realistic component group for meso choices, and close-ups in context for micro choices.
Use fictional sample content and local HTML/CSS; do not embed external assets, trackers, live actions, or raw user-supplied markup.
Check that all options stay readable, keyboard accessible when selectable, and comparable at narrow and wide widths.
Never trade contrast, focus visibility, or required UI behavior for a preference.

## Review and save

1. Combine the decisions into one representative HTML preview, show it in the same tab as above, and summarize the confirmed rules by layer.
2. For refinement, show the before and after on the same content and name what stays unchanged.
3. Separate confirmed preferences from unresolved or unasked items; do not turn a skipped choice into a rule.
   - If no preference was confirmed, do not create an empty style or rewrite the base style.
4. Ask for confirmation of the preview, style name, and destination before creating or updating the saved style.
   - If a symlink changes where the destination points, show the resolved path as well.
   - For a new style, require an unused directory; do not overwrite an existing skill.
5. Write the style skill only after confirmation, or retain only the draft if the user pauses or cancels.
6. Check that the saved skill has valid frontmatter, uses the confirmed choices without contradictions, and can stand alone without the interview files.
7. Report the saved skill path and how to reuse it, or report the draft path and how to resume if nothing was saved.
