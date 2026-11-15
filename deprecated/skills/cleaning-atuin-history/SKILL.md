---
name: cleaning-atuin-history
description: Audit Atuin history for duplicate pressure and high-confidence typo/retry pairs, then prepare fixed-scope deduplication or user-run inspector steps without direct SQLite deletion. This deprecated internal workflow keeps cleanup-typos disabled.
metadata:
  internal: true
---

# Atuin History Cleanup (Deprecated Reference)

Audit first. Do not treat a preview, uniqueness estimate, or skill invocation as deletion approval.

## Guardrails

- Resolve the active database with `atuin info` and use the bundled audit before proposing mutation.
- Never delete rows directly from SQLite or edit Atuin config as part of this workflow.
- `atuin history dedup` mutates the selected history window globally.
- `atuin search --delete` deletes every match under active search semantics; do not use it manually for a single row.
- The transactional typo command snapshots the database but also runs `atuin store push`, recomputes and deletes candidates, may drive a TUI, and finishes with `atuin sync`. Its current interface cannot bind execution to approved candidate IDs or guarantee non-interactive operation.
- Do not invoke `cleanup-typos` through this skill. Keep it disabled until it gains a plan-only output plus approved-ID and non-interactive execution checks; its source and recovery artifacts remain historical reference material.
- Re-run the audit and matching dry run immediately before every mutation, whether user- or agent-executed. Use a fixed cutoff instead of a relative value such as `now`; if candidates, scope, or counts differ from the approved set, stop for renewed approval.
- Do not auto-restore a full live database after failure; preserve live state, snapshot, and verification artifacts for recovery.
- The interactive inspector is user-run. An agent must not open or drive its TUI.

Read `references/atuin-cli.md` when exact dedup, search, or prune semantics matter.

## Audit

Resolve this skill directory and run the script by absolute path:

```bash
uv run python "$SKILL_DIR/scripts/atuin_history_cleanup.py" audit
```

Use `--format json` for structured review.
Optional scope flags include `--db-path`, `--dupkeep`, `--before`, `--typo-window-seconds`, and `--max-typos`.
Cutoffs are rounded down to whole seconds so native Atuin commands and audit filtering use the same scope; use the reported `scope.before_iso` as the fixed cutoff for preview and approval.

The audit reads selected history columns, groups duplicates by command/cwd/host, and proposes typo pairs only when session, time, arguments, exit status, frequency, and edit-distance evidence align. Treat its output as candidates, not proof that deletion is wanted.

## Prepare Cleanup

### Duplicates

Resolve the audit's `--before` value to a fixed cutoff, then run the reported `atuin history dedup --dry-run ...` and present the exact window, keep count, groups, and potential deletion count. Immediately before applying, repeat the audit and matching dry run with that same fixed cutoff. Run the identical non-dry command only when the results still match the approved scope and loss; otherwise obtain renewed approval.

### Typos

Present each candidate ID, timestamp, cwd, original, correction, and reason. The supported path is the **user-run inspector**: give the user the prefix/cwd preview, candidate details, and inspector keys so they can confirm and delete the exact row themselves.

Do not offer or execute the bundled transactional command as an approved automation path. It can run `atuin store push`, delete a recomputed set, open a TUI, and run `atuin sync` in one invocation before an agent can verify that the executed plan matches the reviewed IDs.

## Verify

Stop after the approved cleanup. Re-run the same audit scope and report remaining counts. If diagnosing a historical transactional run, preserve `pre_audit.json`, `plan.json`, `post_verify.json`, and the snapshot path; report remote-sync and recovery status without exposing unrelated history.
