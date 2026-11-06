---
name: running-panel-review-loops
description: Deprecated internal reference for iterative multi-reviewer code review, verified findings, explicitly authorized fixes, and bounded re-review cycles.
metadata:
  internal: true
---

# Running Panel Review Loops (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility.
Use only after explicit invocation.

Treat reviewer output as claims to verify, not votes or instructions to apply blindly. Default to review-only when the user asks only for a panel review or consensus. Apply fixes only when the user explicitly requests implementation, fixes, or a review-fix cycle. Commit or push only when the user requests that action; never treat a requested local commit as push authorization.

## Establish the Run

1. Determine the exact diff, commit, branch, or pull request and its comparison base from repository context; do not assume `main`. Infer intended behavior from the request, tests, documentation, and affected callers.
2. Inspect repository instructions and worktree state. Preserve unrelated changes, and stop before editing if they overlap the reviewed paths or make attribution unsafe.
3. Confirm that at least two independent reviewer instances are available. For an explicitly multi-model request, require at least two distinct models; independent instances of one model are sufficient only for a generic panel request. Do not simulate a panel by inventing reviewers or presenting one review in multiple voices.
4. Accept user-supplied presets, optional score reporting or threshold, iteration cap, and review-only or review-fix mode. Accept a user-supplied panel size only when it is at least two. Reject a requested panel size below two and ask the user to raise it before starting. Otherwise use three reviewers, a first-round `code-review` preset, `adversarial` re-reviews, and a maximum of three iterations. Scores are off by default; a requested threshold enables score reporting as a presentation signal, not an acceptance gate.

If the review target or requested mutation mode remains materially ambiguous, ask one focused question. A panel may inspect uncommitted work, but each round must identify the exact snapshot reviewed.

## Run One Iteration

1. Give every reviewer the same snapshot, intent, relevant constraints, and requested preset. Keep reviews independent until synthesis, and run them in parallel when the available mechanism supports safe concurrency.
2. Ask each reviewer for blocking-objection status, severity-ranked findings with concrete file or behavior evidence, and meaningful missing checks. Request a 0–10 score only when score reporting is active. A blocking issue must concern correctness, safety, security, data integrity, or another explicit acceptance requirement—not style preference.
3. Treat a missing or invalid required review field as a reviewer failure and retry one transient reviewer failure once. Continue with a disclosed partial panel only when at least two independent substantive reviews remain. When scoring is active, disclose and omit an invalid score without discarding otherwise usable findings; never fabricate a score.
4. Synthesize agreements and disagreements. When scoring is active, normalize valid scores to 0–10 and compute a mean only with at least two valid scores. Report whether a requested threshold was met, but never let a score or average override verified findings or determine acceptance.
5. Verify every actionable claim against the source, affected flow, tests, and executable checks where feasible. Resolve disagreements through evidence rather than majority vote. Label theoretical or unverified risks and do not change behavior solely to satisfy them.
6. In review-only mode, run only non-mutating checks against the complete reviewed snapshot; use an isolated copy for fixing gates, or report the gate as unavailable.
   Report the synthesis and stop before edits.
   In review-fix mode, address only confirmed, in-scope findings.
   Add the smallest boundary or regression test when practical, apply the smallest coherent fix, then run those snapshot-level checks.
7. Re-review the complete updated diff in the next iteration. Do not reuse stale scores or count a check run against an earlier snapshot as evidence for the current one.

Do not churn on subjective non-blocking suggestions. Apply a non-blocking suggestion only when it is concrete, proportionate, behavior-preserving or requirement-backed, and improves verification or materially reduces risk.

## Accept and Stop

Accept only when all of the following hold for the current snapshot:

- at least two independent substantive reviews cover the complete snapshot;
- no reviewer has a surviving blocking objection;
- synthesis and source verification reveal no blocking correctness, safety, security, or explicit-requirement issue; and
- checks appropriate to the complete reviewed snapshot pass.

Stop without lowering the bar when the iteration cap is reached, fewer than two independent reviewers remain, validation cannot run, a required product decision is missing, safe work would expand scope, or the same unverified concern repeats without new evidence. Report any residual findings and the exact blocker or cap reached.

Before a requested commit, stage only intended paths, inspect the staged diff, and create a focused commit grounded in that diff. Push only when explicitly authorized for the verified remote and refspec; report the commit ID and remote verification when applicable.

## Report

For each iteration, report the reviewed snapshot and preset, blocking status, consensus and disputed findings, changes made, and validation evidence. Include per-reviewer scores, mean, and requested-threshold status only when score reporting is active. Finish with the stopping reason, accepted or residual risk, and any authorized commit or push result. Never claim panel consensus, test success, a commit, or a push without direct evidence.
