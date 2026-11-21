---
name: prune-code-comments
description: Audit or prune source-code comments across a codebase or a specified area. Use when asked to remove redundant or stale comments, turn workarounds into issues, move decision rationale into ADRs, enforce a gradual ban on new comments, or estimate how many source lines comment removal would save. Not for PR review comments or ordinary code review.
---

# Prune Code Comments

Review every source comment in the requested scope using a tokenizer or parser for each language.
Keep required notices, tool directives, and public API documentation; defer comments whose meaning is unclear.
If asked only to audit, plan, or estimate, do not make changes.

## Classify and Act

| Category | Meaning | Action |
| --- | --- | --- |
| Tautology | Repeats what the code already shows. | Delete it. |
| Excuse | Justifies a workaround that still needs a fix. | Capture it in a follow-up issue before deleting the comment; leave the workaround unchanged. |
| Stale | Describes something that no longer applies. | Verify, then delete it. |
| Decision Record | Explains an important, non-obvious choice. | Move the rationale to an architecture decision record (ADR) before deleting the comment. |

Reuse an existing issue or draft one if filing is not authorized.
Keep the comment if deleting it would lose a live warning with no durable handoff.

## Enforce the Ban

Use a syntax-aware linter for the same scope, implemented in a language that fits the project’s tooling.
Add it to the project's pre-commit hook setup.
Baseline only the remaining non-exempt comments and shrink the baseline as they are removed.
Reject new or edited comments, even if the total stays the same, and do not allow the baseline to grow after setup.
Verify through the hook that retained comments pass and new or replacement comments fail.

## Report

Summarize category counts, exceptions, deferrals, issue and ADR references, and verification results.
Report the all-comments upper bound, the estimated removable lines, and the actual lines removed.
Count only physical source lines occupied entirely by comments: removing an inline comment does not save a line.
