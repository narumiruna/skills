---
name: refine-docs
description: Improve existing documentation for clarity, concision, and structure. Use to polish wording, reorganize sections, or remove repeated ideas within or across specified files or folders (Markdown by default). Do not use to create new documents, change their substance, or verify claims against code.
---

# Refine Docs

Work only on the specified files and folders, including subfolders.
Process Markdown (`.md`) unless the user selects another format.
Honor narrower requests: if asked only to remove repetition, do not rewrite or reorganize other content.
Apply edits directly unless the user asks only for findings.
Do not stage or commit changes.

## Workflow

1. **Read:** Identify each document's purpose, audience, and task order.
   Save the pre-edit contents so the diff excludes earlier changes.
2. **Refine:** Make the smallest changes that address the request.
   - Replace unclear or wordy phrasing with direct language.
   - Move or group related content when this makes instructions easier to find or follow.
   - Find repeated ideas, even when phrased differently or spread across files.
     Remove duplicates or merge overlaps without losing unique details.
     Keep repetition that a document needs to stand on its own.
   - Preserve the original meaning, facts, requirements, conditions, and exceptions.
     Do not guess when the documents leave an ambiguity or contradiction unresolved.
3. **Verify:** Reread the edited passages in context and review the diff.
   Check that prerequisites still come first, links and heading references still work, and unrelated content is unchanged.
4. **Report:** Use the saved pre-edit contents as the baseline and report only this run's changes.
   Use the format the user requests.
   Otherwise, give a brief Git-style summary in a fenced `diff` block with `-` for before and `+` for after.
   Label it as a summary, not an apply-ready patch.
   If nothing changed, say so instead.
   Report any unresolved issues.
