---
name: iterating-ui-improvements
description: Deprecated internal reference for iteratively auditing and improving an existing web interface through an explicit Chrome DevTools audit-fix-commit loop.
metadata:
  internal: true
---

# Iterating UI Improvements (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility. Use only after explicit invocation. That invocation authorizes an audit-fix-commit loop with in-scope local edits, validation, and local commits; it does not authorize remote or destructive actions.

## Establish the Run

Accept an optional URL, user flow, page scope, stopping mode, and iteration limit. Prefer invocation details. Otherwise inspect repository instructions, application documentation, configuration, existing start commands, tests, and design-system conventions to infer one local site and primary flow. Ask one question only when multiple targets remain plausible.

Require all of the following before changing files:

- a clean Git worktree, including no staged, unstaged, or untracked changes, and an attached symbolic branch that will retain each commit; detached HEAD is a blocker, and do not create or switch branches without authorization;
- an available Chrome DevTools capability and a reachable target that can be started through established non-interactive project commands;
- any required test, account, or authentication context already available without bypassing controls; and
- enough product evidence to preserve existing behavior, data meaning, permissions, recovery paths, and unrelated capability.

Stop and report the blocker when a prerequisite fails. Do not substitute another browser tool silently, guess credentials or product intent, or alter data to gain access.

Determine whether the target is already running. If this run starts it, record process or job ownership needed to stop its server and child watchers later; do not claim ownership of a pre-existing target.

## Choose the Finding Threshold and Limit

- **`substantial` (default threshold):** continue while there is an evidence-backed, medium- or high-value problem affecting task completion, usability, or accessibility. Stop rather than pursue low-impact polish or subjective taste.
- **`exhaustive`:** also address low-impact UI problems when they are concrete, evidence-backed, and verifiable. Do not pursue unsupported subjective preferences.
- **`fixed N`:** apply the specified positive iteration cap to the active finding threshold. If no threshold is named, use `substantial`. Stop earlier only when no finding meets the active threshold, and report known remaining findings when the cap is reached.

There is no iteration limit by default. A user may set a positive limit with either threshold; the limit applies to the active finding threshold. Never interpret an omitted limit as five or another implicit cap.

## Run One Iteration

1. Use Chrome DevTools to reproduce the primary task and collect baseline evidence. As relevant to the target, inspect visual hierarchy, critical interactions, representative wide and narrow viewports, keyboard operation, semantic accessibility, and related console or network failures.
2. Rank findings by user impact, confidence, scope, and reversibility. Select one highest-value, coherent improvement theme that meets the active stopping mode. If none qualifies, stop without creating an empty commit.
3. Record the iteration plan in the execution log: observed evidence, user impact, exact change boundary, and acceptance checks. Do not add a plan file to the product repository.
4. Implement the smallest coherent improvement. Preserve unknown behavior, content and data semantics, permissions, cancellation and recovery, and unrelated features. Stop before a product decision or material scope expansion.
5. Run the repository's focused checks for the affected behavior. Re-verify the same flow and representative viewports in Chrome DevTools, confirming the improvement and checking for related interaction, responsive, accessibility, console, and network regressions.
6. Only after verification passes, stage only the paths changed for this iteration, inspect the staged diff, and record the staged tree identity. Create one focused Conventional Commit grounded in that diff, then compare the committed tree with the recorded staged tree before accepting the commit. Verify the commit ID and a clean worktree before beginning another iteration.

If successful hooks changed the tree, treat their committed result as unverified and rerun affected checks and Chrome DevTools verification against the committed content. Accept it only if those checks pass. If they fail, restore the recorded validated tree, revalidate it, and create a clearly labeled recovery commit without rewriting history; verify that recovery commit's tree, then stop and report both commit IDs. If restoration or the recovery commit cannot be completed safely, stop and report the exact branch, index, and worktree state.

If commit creation fails, preserve the hook or error output and re-inspect the index and worktree. Do not bypass hooks with `--no-verify`. Correct only an in-scope cause, rerun affected checks and Chrome DevTools verification when files changed, then retry. If a valid commit still cannot be created safely, unstage the exact iteration paths and apply the failure recovery below.

Repeat from the observed post-commit interface rather than reusing stale findings.

## Handle Failure and Stop

If implementation cannot pass its checks within the current coherent scope, or a valid commit cannot be created, unstage the exact iteration paths, restore only the current iteration's uncommitted tracked changes, and remove only files created during that iteration. Preserve every earlier successful commit. Do not reset, amend, rebase, or otherwise rewrite prior commits. If safe restoration cannot be proved or completed, stop and report the exact index and worktree state.

Stop when the active finding threshold is empty, a fixed or explicit limit is reached, Chrome DevTools or tests are blocked, commit creation fails without a safe in-scope correction, a required product decision is missing, safe work would expand scope, or restoration fails. Do not push, open a pull request, deploy, mutate remote services, perform destructive data operations, or broaden the target without separate explicit authorization.

Before every exit, including success and blocked or failed paths, terminate and wait only for target processes started by this run and their child watchers. Preserve a target that was already running. If owned-process cleanup fails, report the remaining process and port evidence rather than stopping unrelated processes.

Report each iteration's plan, commit ID, and validation evidence, followed by the stopping reason, cleanup result, and any known unaddressed findings. Distinguish verified outcomes from untested states or assumptions.
