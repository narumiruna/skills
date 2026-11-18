---
name: improve-agent-harnesses
description: Run or resume a measured agent harness optimization loop with Self-Improvement Memory (SIM) when asked to improve how an agent uses prompts, context, tools, or execution flow, including after a model or benchmark change.
---

# Improve Agent Harnesses

Improve the harness around a fixed task-solving model without training the model.
Use Self-Improvement Memory (SIM) to help the proposer and selector reuse the evidence behind earlier harness edits.

## Set up the run

- Identify the harness revision and files in scope, the exact model version, the benchmark or local checks, and the available execution budget.
- Use an existing local run directory or confirm where to save the run if none is specified.
- Pin the model, evaluator, task split, and run settings for all comparisons within the run.
- Before scoring candidates, define the metric, minimum gain over the current round's baseline, allowed regressions, and any run-level score target.
- Set a round limit, candidate limit per round, and execution timeout; default to at most two rounds and two candidates per round.
- Use only development tasks (the evolve set) for diagnosis, selection, memory updates, and stopping decisions.
- If available, reserve separate held-out tasks for final evaluation; skip them if their tasks or results cannot be kept out of the optimization loop.
- Work on isolated local copies with restricted tool access, no production credentials, and network access disabled by default.
- Do not modify the live harness, this skill, standing instructions, or tool permissions as part of the loop.
- Obtain separate approval before paid or networked evaluations, wider scope, or deploying a retained edit.

## Run the evaluator, proposer, and selector loop

1. **Evaluate the retained harness.**
   Run it on the evolve set and save scores, relevant traces, and errors in the run history.
2. **Propose candidate edits.**
   Read the retained code, run history, and full SIM snapshot to diagnose the current failure.
   For each candidate, cite an existing root-cause hypothesis or name a new one, explain the edit, and record the specific failures it should fix before testing.
   Revisit a tried direction only when new evidence or a changed setting warrants it.
3. **Screen, evaluate, and select.**
   Read the same SIM snapshot and reject candidates that exceed scope, change the evaluator, or satisfy the metric without solving the task.
   Evaluate the remaining candidates separately from the same retained revision, using the baseline's tasks, scoring, and execution settings.
   Select at most one candidate that meets the acceptance criteria, weighing the measured gain against complexity and regression risk.
   If none qualifies or the evidence is inconclusive, keep the current harness and leave SIM unchanged.
4. **Checkpoint the result.**
   Append only the selected edit to SIM, and keep its missed predictions or regressions even if the edit is later replaced or removed.
   Keep unselected trials and their evidence in the ordinary run history, not SIM.
   Save the retained revision, SIM, and round number together before starting another round.
5. **Stop when the run reaches its score target or exhausts its budget.**
   If the evaluator or isolation fails, stop and report the blocker instead of weakening the run controls.
   Once selection is frozen, compare the starting and retained harnesses on the held-out set if it was reserved.
   Keep held-out results out of SIM and future tuning, and label evolve-only results as such.

## Write and reuse memory

- Store SIM separately from the runnable harness and raw logs, in one local JSON file such as `sim.json`.
- Key each entry by a stable ID and a root-cause hypothesis, not by a task ID or filename.
- Append attempts to the matching entry without overwriting earlier evidence; merge identical hypotheses only if all attempts and their original provenance are preserved.
- Record the edit and rationale, affected files and revision, predicted fixes, observed fixed and missed tasks, scores and regressions, and a reference to the evidence.
- Include the run ID, round, model version, benchmark, and evolve split in every attempt so results are interpretable after transfer.
- Treat SIM and traces as data for the optimizer, not instructions for the task-solving model.
- Redact sensitive data rather than copying raw logs or credentials into memory.

Start a fresh run with empty SIM.
To resume the same run, load the saved checkpoint and verify that the settings still match.
To continue in a new setting, carry forward the retained harness and SIM only if the harness interface is compatible.
For a controlled transfer, change either the model or the benchmark, and measure the inherited harness in the target setting before editing it.
Use earlier diagnoses and outcomes as hypotheses, not proof that an edit still works in the target setting.
To measure the benefit of SIM itself, compare continuation runs with the same starting harness, target setting, and budget, with and without SIM.

Report the starting and retained revisions, comparable results and regressions, and the paths to the run history and SIM.
Distinguish observed improvement from unverified predictions.

Based on [Self-Improvement Memory Enables Continual Recursive Self-Improvement](https://arxiv.org/html/2611.18856v1), Figure 1, Section 3, and Appendix D.
