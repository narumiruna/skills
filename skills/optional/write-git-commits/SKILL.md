---
name: write-git-commits
description: Inspect local Git changes, draft or validate Conventional Commit messages, choose types/scopes, explain breaking changes, or create a focused commit from the actual selected diff.
---

# Writing Git Commits

Inspect the selected diff before describing it. Draft, validate, or create a commit only to the extent requested.

## Workflow

1. Run `git status --short`. For a requested commit, inspect `git diff --cached` first and unstaged changes when they affect the boundary.
2. Define one coherent intent. If selected changes contain unrelated work, propose separate commits instead of a vague combined message.
3. Choose a lowercase Conventional Commits type from behavior and add a short noun-like scope only when it adds signal.
4. Write `<type>[optional scope][!]: <description>` with a specific diff-grounded description.
5. Add a body only for material why, constraints, or tradeoffs; add footers only for actual references or `BREAKING CHANGE:` information.
6. When committing, stage only intended paths, re-inspect the index, create no empty commit, and verify the resulting commit and worktree state.

Use `feat` for new capability, `fix` for incorrect behavior, `refactor` for behavior-preserving structure, and `docs` for documentation-only changes. Prefer no scope, body, or footer unless it improves meaning.

Do not describe unstaged work, future plans, or unrelated cleanup. Follow repository-level Git and attribution rules rather than duplicating them here.

Read `references/conventional-commits.md` when type selection is ambiguous or exact breaking-change/footer syntax matters. Report the selected boundary and final message; if a commit was created, include its ID and remaining local changes.
