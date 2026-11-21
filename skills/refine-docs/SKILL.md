---
name: refine-docs
description: Improve existing documentation for clarity, concision, and structure. Use to polish wording, reorganize sections, or remove repeated ideas within or across specified files or folders (Markdown by default). Do not use to create new documents, change their substance, or verify claims against code.
---

# Refine Docs

Work only on the specified files and recursively on the specified folders.
Process Markdown (`.md`) by default unless the user selects another format.
Honor narrower requests: if asked only to remove repetition, do not otherwise rewrite or reorganize.
Apply in-scope edits directly unless the user asks only for findings.
Do not stage or commit changes.

## Workflow

1. **Read:** Identify each document's purpose, audience, and task order.
   Save the current contents before editing so the final diff excludes earlier changes.
2. **Refine:** Make the smallest changes that address the request.
   - Replace unclear or wordy phrasing with direct language.
   - Move or group related content when this makes instructions easier to find or follow.
   - Compare repeated statements by meaning, including across files.
     Remove an equivalent statement or merge partial overlaps without losing unique details.
     Keep repetition needed for a document to work on its own.
   - Preserve the original meaning, facts, requirements, conditions, and exceptions.
     If an ambiguity or contradiction cannot be resolved from the documents, flag it rather than guessing.
3. **Verify:** Reread the edited passages in context and review the diff.
   Check that step order still respects prerequisites, that links and heading references still work, and that unrelated content is unchanged.
4. **Report:** Summarize the edits and any unresolved issues, then show the unified Git diff for this run only.
   Use `git diff --no-index` against the pre-edit contents if `git diff` would include earlier changes or miss an edited file.
   If nothing changed, say so instead of showing an empty diff.
