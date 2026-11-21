---
name: prune-docs
description: Use only when the user explicitly invokes prune-docs to compare documentation with repository code and directly remove or simplify redundant, conflicting, outdated, or overly detailed implementation claims without changing code.
---

# Prune Docs

Reduce documentation maintenance for AI coding agents by keeping information that cannot be reliably reconstructed from code.
Run only on explicit invocation, which authorizes in-scope documentation edits without further confirmation.
Review the entire repository unless the user narrows the documentation scope.
Search the repository for relevant implementation evidence even when the documentation scope is narrower.
Edit documentation files only.
Do not create commits unless explicitly requested.

## Workflow

1. **Discover** documentation files in scope and inspect the working tree for existing user changes.
2. **Extract** independently verifiable claims with their document paths and line numbers.
   Preserve qualifiers that determine when each claim applies.
3. **Trace** each claim to specific paths and lines in source code, configuration, schemas, or tests.
4. **Verify** actual behavior on the applicable code paths and under the relevant defaults and conditions.
   Treat code as authoritative for implementation behavior.
   Require concrete evidence of a semantic match or contradiction rather than relying on similar wording, names, comments, or isolated declarations.
   Check implementation history when needed to verify that behavior was removed or superseded.
   Treat an unsuccessful search as insufficient evidence, not proof that a feature is absent.
5. **Classify** each claim using the table below.
6. **Modify** documentation according to the classification.
   Capture each file's working-tree contents before editing so the final diff excludes earlier changes.
   Preserve existing user edits and report any finding you cannot apply without disturbing them.
   Prefer deletion to restatement, but preserve the meaning of any unique intent, rationale, trade-offs, and external constraints.
   Delete a section or file if no meaningful content would remain after pruning.
   Keep remaining headings, links, and surrounding prose usable without unrelated reformatting.
7. **Report** after checking that the diff contains only intended documentation edits and that each edit has supporting code evidence.

## Classifications

| Classification | Criteria | Action |
| --- | --- | --- |
| `DUPLICATE` | Fully and reliably derivable from code with no unique information | Remove the claim. |
| `REDUCIBLE` | Contains both reliably derivable details and unique information | Remove only the redundant details. |
| `IRREDUCIBLE` | Contains necessary information that cannot be reliably derived from code | Keep it. |
| `OUTDATED` | Verified evidence shows that the claim once applied but no longer applies to the documented version or scope | Delete a wholly outdated document; otherwise delete only the outdated claims. |
| `CONFLICT` | Contradicts verified implementation behavior and does not meet `OUTDATED` criteria | Remove the contradicted claim instead of rewriting it to match code. |
| `NO_CODE_MATCH` | Insufficient evidence to establish a relationship to code | Keep it and report it as unresolved. |

Distinguish expensive reconstruction from uncertain reconstruction.
Do not keep reliably derivable details solely to save exploration time, tokens, or effort.

## Output

- **Summary:** List changed files and counts for every classification in the table, using the labels exactly as written.
- **Changes:** Explain what was removed or simplified and cite the supporting code paths and lines, including commit IDs when relying on implementation history.
- **Diff:** Show the unified Git diff for this run's edits only.
  Use one fenced `diff` block per changed file, labeled with its repository-relative path.
  Include hunk line numbers and nearby context so readers can locate each change.
  Use `git diff --no-index` against pre-edit snapshots if the normal Git diff would include pre-existing changes or omit an edited untracked file.
  Show repository-relative file names in diff headers instead of temporary snapshot paths.
  If nothing changed, say so instead of showing an empty diff.
- **Unresolved:** List unverified claims and evidence gaps, plus any edits skipped to preserve user changes.

Omit other unchanged claims from the detailed report unless they affect the outcome.
