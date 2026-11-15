---
name: improve-codebase-architecture
description: Assess or improve an existing codebase's architecture when the user asks about module boundaries, coupling, scattered ownership, testability, change locality, deep modules, seams, or behavior-preserving structural refactoring. Use for cross-module design rather than ordinary diff review or a confirmed edge-case bug fix.
---

# Improving Codebase Architecture

Find evidence-backed structural improvements that concentrate behavior and ownership behind smaller, clearer interfaces. Treat review, assessment, diagnosis, and planning requests as read-only. Improvement, refactoring, or implementation requests authorize in-scope local edits and non-destructive validation. Require confirmation before external writes, destructive actions, an incompatible public API or data migration, or material scope expansion.

## Establish Scope

1. Read repository instructions and the domain glossary, architecture documents, and ADRs relevant to the target. Missing optional architecture documents are not blockers.
2. Use the area, pain point, or behavior named by the user. Trace only its actual callers, contracts, dependencies, data and state ownership, tests, and directly affected runtime paths.
3. When no target is named, inspect recent change history and repeatedly modified paths to bias the assessment toward architecture where future work is likely. Widen the scan only when no meaningful hotspot emerges.
4. If multiple incompatible directions remain equally plausible, or the work would break a public API, require a migration, or cross the requested boundary, ask one focused question before choosing.

## Assess

Load [the architecture assessment reference](references/architecture-assessment.md) when evaluating candidates.

- Observe concrete friction: concepts split across files, callers coordinating the same policy, state with unclear ownership, wide or unstable interfaces, leaking dependencies, duplicated adaptation, or tests that must bypass the intended interface.
- Measure the interface by everything callers must know, including ordering, invariants, errors, configuration, side effects, and performance—not only method count.
- Apply the deletion test: reject a proposed module when deleting it would only move the same complexity into callers. Reject speculative seams, pass-through abstractions, style-only rearrangement, and abstractions without a demonstrated variation or ownership need.
- Compare the current and proposed ownership, interface, dependency direction, test surface, and migration path. Prefer the smallest structural change that improves locality or leverage without hiding important operational behavior.
- Keep claims tied to source, tests, history, or executable evidence. Label assumptions and unverified risks.

For an assessment-only request, return at most three candidates ordered by expected leverage, migration risk, and confidence. For each, include evidence paths, current friction, proposed seam and ownership, expected locality or leverage, migration risk, and a concrete verification method. Name the top recommendation and explain why it outranks the alternatives. Do not create a visual report unless the user asks for one.

## Refactor Safely

For an authorized implementation request:

1. Select one highest-confidence, bounded candidate. Do not bundle unrelated cleanup.
2. Establish a behavioral baseline with existing checks and, when practical, characterization or regression coverage at the current public contract.
3. Move ownership in small, reversible steps. Preserve externally observable behavior and existing contracts unless the request explicitly changes them; keep the worktree runnable between steps when practical.
4. Put policy at its owning module and adapt dependencies at the narrowest justified seam. Remove superseded paths instead of leaving parallel abstractions.
5. Run focused checks after each meaningful step, then affected integration tests and the repository gate. Reinspect callers, dependency direction, tests, and the final diff to confirm the candidate's claimed benefit was actually achieved.
6. Stop after the selected candidate is complete. Report changed ownership and interface, behavior evidence, checks run, residual risk, and any stronger candidate deferred because it needs a product or migration decision.

Use `review-code` for ordinary diff or pull-request correctness review. Use `harden-code-paths` for confirmed edge-case and failure-mode bugs; an architecture finding may explain the root cause, but do not turn this workflow into a generic bug sweep.
