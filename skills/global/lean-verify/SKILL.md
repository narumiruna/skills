---
name: lean-verify
description: Formalize claims and construct or check Lean 4 proofs when mathematical theorems, program properties, algorithm correctness, or other claims need formal verification, using a persistent project under ~/.agents/lean.
---

# Lean Verification

Verify the intended claim, not only a simpler replacement that Lean can prove.

## Define the Claim

1. Identify the claim, its domain, hypotheses, and required conclusion.
2. Inspect the relevant definitions, specifications, and source files before choosing a formal model.
3. For code-related claims, record the source revision or file hashes and explain how the Lean model corresponds to that source.
   - Account for relevant differences such as natural numbers versus integers, overflow, floating-point arithmetic, side effects, and termination.
   - A proof about a handwritten model does not by itself prove the original implementation correct.
4. For explanation or planning requests, report without creating a workspace or installing tools.

## Prepare the Workspace

1. Read [installation and project setup](references/installation.md) before installing tools, initializing a project, or changing dependencies.
2. Use `~/.agents/lean` as the persistent Lean 4 project unless the user specifies another location under `~/.agents/`.
3. Keep verification artifacts outside the target repository unless the user requests integration there.
4. Reuse existing proofs and dependencies without overwriting unrelated work.
5. Choose a unique Lean module and namespace for each task, such as `Verifier/TaskName.lean` and `Verifier.TaskName` in a newly initialized project.
   - For an existing project, follow its library layout instead.
6. Use Lean core and Std when sufficient; add mathlib, CSLib, or Batteries only for definitions or tactics the task needs.

## Formalize and Prove

1. Write the definitions and theorem statements before developing the proofs.
2. Check that each statement matches the original claim and that its hypotheses are meaningful and jointly satisfiable.
3. Search the installed libraries for existing definitions and lemmas before creating replacements.
4. Include each new module in the library's import graph so the project build checks it.
5. Do not weaken the conclusion, strengthen the hypotheses, or change the model just to obtain a proof without explaining and agreeing on that scope change.
6. Do not substitute `sorry`, `admit`, new axioms, or unsafe declarations for a proof.

## Check the Result

Run commands from the verification project root.
Replace example module paths and theorem names with the actual task names.

1. Run `lake build` and inspect the diagnostics for the task modules, not only the exit status.
2. Run `lake env lean Verifier/TaskName.lean` to check the task file directly.
3. Add `#print axioms Verifier.TaskName.claim` for each final theorem and rerun the file to inspect its transitive axiom dependencies.
   - Reject `sorryAx` and unapproved custom axioms, including those hidden in helper lemmas.
   - Disclose standard axioms such as `propext`, `Classical.choice`, and `Quot.sound` when present.
   - Disclose additional trust in evaluators or compiled code, such as `native_decide`; do not describe such a result as ordinary kernel-only checking.
4. Recheck the theorem statements and source correspondence after the final edits.
   - Sample executions, `#eval`, and a successful build alone do not establish the intended claim.
5. If proof checking fails or setup is blocked, report the exact failure and the remaining obligation instead of claiming verification.
   - Distinguish a demonstrated counterexample from an incomplete proof attempt.

## Report

- State whether the claim was proved under stated assumptions, refuted by a checked counterexample, or remains unverified.
- Give the theorem names, absolute artifact paths, and the claim-to-model correspondence.
- Include the Lean version, resolved dependency revisions, commands run, and results.
- List assumptions, axiom dependencies, additional trust, and any gap between the model and the original implementation.
