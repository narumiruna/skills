---
name: remove-doc-repetition
description: Find and remove repeated ideas, claims, or rules within or across specified documents, even when worded differently. Use for semantic deduplication of one file, multiple files, or folders (Markdown by default), not for comparing documentation with code or general copyediting.
---

# Remove Doc Repetition

Work only on the specified files and recursively on the specified folders.
Process Markdown (`.md`) by default unless the user selects another document format.
Apply safe edits directly when invoked, but leave files unchanged if the user asks only for findings.
Do not stage or commit changes.

## Workflow

1. **Extract:** Read each file line by line and identify independent claims, rules, or ideas in context.
   Record their paths, lines, and any conditions or exceptions that affect their meaning.
2. **Compare:** Compare statements by meaning within each file and across the selected files.
   A shared topic or similar wording does not establish overlap.
3. **Classify:** Assign each candidate pair one label:
   - `DUPLICATE`: The statements convey the same information under the same conditions; remove the redundant occurrence if it serves no separate purpose.
   - `PARTIAL_OVERLAP`: The statements share some information but are not equivalent; merge them or trim the repeated information.
   - `UNRELATED`: The statements share no substantive information; leave them unchanged.
4. **Consolidate:** Save the current contents of each file before editing.
   Prefer deletion to rewriting, and preserve all unique information, original intent, conditions, exceptions, and document structure.
   Before removing a cross-file repeat, check each document's purpose and keep repetition needed for standalone use.
   Leave the original text unchanged if you cannot confirm the edit is safe.
5. **Verify:** Reread the changed passages in context and compare them with their pre-edit contents.
   Check that the edits meet the preservation rules above, preserve links, introduce no new repetition, and touch no unrelated content.
6. **Report:** Summarize changes and important candidates left intact, then show the unified Git diff for this run only.
   Generate the patch with `git diff`, or use `git diff --no-index` against the pre-edit contents if `git diff` would include earlier changes or miss an edited file.
   If there are no edits, say so instead of showing an empty diff.
