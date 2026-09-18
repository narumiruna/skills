---
name: apply-tdd
description: "Use when implementing a non-trivial, observable behavior change with TDD under explicit ecosystem production-path and test-isolation boundaries. Do not apply red-first mechanically to static configuration, wiring, metadata, or production code outside the defined boundary."
---

# Applying TDD

Use tests as executable behavior specifications, not as a coverage ritual.

## Scope the Boundary

Before writing a test:

1. Load [test boundaries](references/test-boundaries.md), resolve the repository's actual production and test layouts from its manifests, package configuration, imports, runner configuration, and established paths, then apply the matching ecosystem fallback only where that evidence is insufficient. More-specific repository instructions override the fallback.
2. Partition eligible work by observable behavior rather than by file.
3. Apply TDD to a work unit only when all are true:
   - it changes a contract observable at a stable boundary
   - a focused test can fail for the intended reason before implementation
   - the test would catch a plausible regression that cheaper validation would not catch as clearly

Treat supporting edits such as config, wiring, schemas, fixtures, and generated artifacts as part of the behavior slice, not as separate units that each require a red-green cycle. Test custom parsing, defaults, validation, precedence, or resulting runtime behavior; do not write a test that merely repeats static config values, standard framework declarations, or metadata.

If no meaningful behavior contract exists, skip TDD and use the cheapest proportionate check: parse or schema validation, compile or type checking, linting, a focused smoke check, an existing integration test, or the repository gate. Do not add production abstractions solely to make a low-risk declarative edit unit-testable, and do not require an exception report for work that is outside this boundary.

## Cycle

1. Identify the smallest observable behavior that should change.
2. Add or update the narrowest test at a stable boundary that proves the behavior. Control time, randomness, network, storage, and other external inputs so the test is deterministic and isolated.
3. Run it and confirm the intended test executes and fails for the intended reason. Discovering zero tests is not a red state. If the test passes, correct it or establish why another check is the valid red state.
4. Implement the smallest change that makes the test pass. Do not weaken or delete a correct test to accommodate the implementation.
5. Run the focused test, then relevant integration or end-to-end coverage and the repository gate.
6. Refactor only while tests are green and without changing behavior.

For a bug, add a regression test when feasible. For a multi-path change, repeat the cycle in small observable increments rather than writing the entire implementation first.

## Exceptions

Pure formatting, comments, behavior-preserving renames, exploratory spikes, visual-only styling, and declarative edits with no custom behavior are outside the normal TDD boundary. Requirements may also be too uncertain to encode safely.

When a non-trivial behavior change cannot start with a failing test, state:

- why the red state was impractical or unavailable
- how behavior was verified instead
- what risk remains

Finish with the behavior proved, the initial failure evidence when available, and the passing checks. Do not claim TDD merely because tests were added after implementation.
