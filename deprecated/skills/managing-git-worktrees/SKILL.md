---
name: managing-git-worktrees
description: Deprecated internal reference for creating, inspecting, attaching, repairing, removing, or pruning local Git worktrees while preserving branches, commits, files, and submodule data.
metadata:
  internal: true
---

# Managing Git Worktrees (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility. Inspect before mutation. Keep worktree operations separate from commits, pushes, rebases, and unrelated branch changes. Treat dynamic refs and paths as untrusted: validate them, pass them as argv when possible, and quote shell values.

## Inspect

1. Capture the invoking worktree, symbolic branch, and HEAD. A detached invoking HEAD requires an explicit creation start point.
2. Parse `git worktree list --porcelain -z`; the first record identifies the main worktree. If it is bare or stale, request a storage root or repair it before deriving paths.
3. Resolve the requested branch, path, and start point. Never assume the default branch name.

For a new path, default the storage root to `$HOME/.worktrees`; if `$HOME` is unset or unusable, request an explicit root. Create the root if absent, then use `<root>/<main-name>-<branch-with-slashes-replaced-by-hyphens>`. Stop on an existing path or normalization collision rather than inventing a suffix.

## Create or Attach

1. Normalize the branch with `git check-ref-format --branch "$branch"` and resolve the start point to one commit with `git rev-parse --verify --end-of-options "${start_point}^{commit}"`.
2. Determine exact branch existence with `git show-ref --verify` and occupancy from porcelain records; do not substring-match.
3. Create or attach:

```bash
git worktree add -b "$branch" "$worktree_path" "$start_oid"  # new branch
git worktree add "$worktree_path" "$branch"                  # existing free branch
```

Stop if the branch is checked out elsewhere; do not bypass occupancy with `--force`. Verify the exact record and `git -C "$worktree_path" status --short --branch`.

## Remove Safely

1. Confirm the exact target is a registered linked worktree, not the first/main record.
2. Inventory all data:

```bash
git -C "$worktree_path" status --porcelain=v1 --untracked-files=all --ignored=matching --ignore-submodules=none
```

Expand directory entries when needed and inspect initialized submodules recursively. Every tracked, `??`, and `!!` entry can be lost.
3. For detached targets, record HEAD and check reachability:

```bash
git for-each-ref --format='%(refname)' --contains="$head_oid" refs/heads refs/tags refs/remotes
```

Preserve an otherwise unreachable commit with a user-named branch or tag before removal.
4. Stop on a lock. Unlock only after explicit confirmation that the lock is no longer needed.
5. If loss inventory is empty and reachability is safe, run `git worktree remove "$worktree_path"` and verify its record disappeared.
6. If local-only data exists, display the complete loss and require approval that names it. Use `--force` only when Git requires it and that exact loss was approved; ignored data may disappear even without `--force`.
7. Preserve the branch by default. Never delete the directory directly as a substitute for `git worktree remove`.

## Branch Deletion

Delete only when separately requested. Resolve the branch and user-chosen comparison ref to commits and prove ancestry with `git merge-base --is-ancestor`. Reverify the branch still points to the inspected object, then try `git branch -d`.

If the branch is unmerged or `-d` checks a different upstream/current-HEAD relationship than the chosen comparison, explain the mismatch. Use `git branch -D` only after separate approval to discard or bypass that exact condition and after rechecking object identity and ancestry.

## Repair or Prune

Use `git worktree repair` for moved worktrees and verify every repaired record. A missing path is not proof that its data should be abandoned.

Prune only when the directory is genuinely gone and recovery is not wanted. Protect detached commits as above, preview with `git worktree prune --dry-run --verbose`, show the exact preview, then run the matching prune only after approval. Pruning metadata is not directory or branch deletion.
