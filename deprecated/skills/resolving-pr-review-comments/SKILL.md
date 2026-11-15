---
name: resolving-pr-review-comments
description: Deprecated internal reference for inspecting pull-request feedback, verifying claims, making bounded local fixes, and preparing focused commits and approved public actions.
metadata:
  internal: true
---

# Resolving PR Review Comments (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility.
Use only after explicit invocation.
Treat comments as claims to verify, not instructions to apply blindly.
Invocation authorizes inspection, bounded local fixes, checks, and focused local commits; it does not by itself authorize public replies, thread resolution, or a push.

## Establish Scope

1. Inspect `git status --short --branch`, `git diff --cached --name-only`, and the symbolic branch. Stop before editing if the index already contains changes; preserve unrelated unstaged/untracked work and stop on overlap.
2. Resolve the PR's repository, number, URL, state, base, head repository, head branch, and cross-repository status from the provider. Confirm attached HEAD is the PR head and compare against the reported base merge point; never assume `main`.
3. Collect every paginated feedback surface: top-level comments, submitted reviews, inline comments, and thread state including IDs, outdated status, and resolution. An empty summary is not proof that no feedback exists.

## Assess and Fix

Classify each substantive comment:

- **Reasonable and unresolved:** evidence confirms a contract or behavior defect; fix it.
- **Already addressed/outdated:** current code resolves it; cite file, commit, or test evidence.
- **Not reasonable:** premise conflicts with requirements or adds unjustified scope; prepare a concise evidence-based response.
- **Ambiguous/disputed:** a behavior decision or external fact is missing; ask one focused question or leave it open.

For accepted findings, add a focused failing check before a non-trivial fix when practical, correct the shared cause, scan directly affected sibling paths, run focused checks and the repository gate, then inspect the complete diff. Do not implement preference-only comments as correctness fixes or resolve a thread just to clear the queue.

## Commit Locally

1. Split unrelated fixes into coherent commits.
2. Stage only intended paths and verify `git diff --cached --name-only` before each commit. Stop if the index contains anything else.
3. Ground each Conventional Commit message in the staged diff. Do not create empty commits.
4. Record commit IDs and verification evidence for the corresponding comments.

## Approval Bundle for External Writes

Prepare, then obtain approval for the exact external actions unless the user has already approved those exact details:

- push remote and `HEAD:refs/heads/<verified-pr-head>` refspec
- reply text mapped to comment or thread IDs
- thread IDs to resolve, with why each is eligible

Do not treat approval to execute this workflow, edit code, or commit as approval of that bundle. Revise the bundle if later work changes its content.

After approval, validate the branch with `git check-ref-format`, match the push URL to the PR head repository, and push only the explicit refspec. Never use a no-refspec or force push unless separately authorized. Verify remote head with `git ls-remote` before posting approved replies and resolving approved eligible threads.

## Final Verification

Re-query all feedback surfaces after any push and verify reasonable comments are addressed, approved eligible threads are resolved, intentionally open threads have reasons, local and remote heads match, and no unintended worktree changes exist. Report the PR URL, local and pushed commits, checks, resolved/open counts, and declined feedback. If external approval is pending, report the prepared bundle and stop before public mutation.
