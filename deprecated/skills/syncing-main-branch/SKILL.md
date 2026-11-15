---
name: syncing-main-branch
description: Deprecated internal workflow for switching a clean Git worktree to local `main` and fast-forwarding it from its configured upstream without losing branches, commits, or local files. Use only when the user explicitly invokes $syncing-main-branch or names syncing-main-branch.
metadata:
  internal: true
---

# Syncing Main Branch (Deprecated Reference)

This workflow is excluded from active discovery but retained for explicit local compatibility. Operate on the current repository and preserve the branch, commits, and files being left.

## Workflow

1. Inspect tracked and untracked state, branch, and HEAD:

```bash
git status --porcelain=v1 --untracked-files=all
git status --short --branch
git symbolic-ref --quiet --short HEAD
```

Stop on any local change; do not stash, commit, discard, or carry it automatically. If HEAD is detached, record it and inspect containing refs. Stop until an otherwise reflog-only commit is preserved with a user-chosen branch or tag.

2. Resolve `main` exactly.
   - Use local `refs/heads/main` when it exists.
   - If absent, create tracking `main` only when exactly one intended remote `main` is clear: `git switch --no-overwrite-ignore --track -c main <remote>/main`.
   - Stop if the remote is ambiguous, `main` does not exist, or another worktree owns it. Do not substitute another branch or bypass worktree protection.

3. Switch with ignored-file overwrite protection when needed:

```bash
git switch --no-overwrite-ignore main
```

4. Verify `main` tracks the intended upstream, fetch its configured remote, then fast-forward only:

```bash
upstream_remote=$(git config --get branch.main.remote)
git rev-parse --abbrev-ref 'main@{upstream}'
git fetch "$upstream_remote"
git merge --ff-only --no-overwrite-ignore 'main@{upstream}'
```

Stop on missing or unexpected upstream, authentication failure, divergence, ignored-file collision, or non-fast-forward. Do not rebase, reset, force, delete files, change upstream, or delete the previous branch.

5. Verify `git status --short --branch` and `git log -1 --oneline --decorate`. Report the active branch, before/after object IDs, upstream, and whether it advanced. “Already up to date” is success and requires no commit.
