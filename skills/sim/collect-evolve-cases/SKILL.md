---
name: collect-evolve-cases
description: Collect reviewed evolve-set cases from one project's local Pi session history for skill improvement. Invoke explicitly to preview, draft, or import cases; never scan in the background.
disable-model-invocation: true
---

# Collect evolve cases

Turn selected historical requests into cases for `improve-agent-harnesses`.
Do not modify sessions, installed skills, SIM, or held-out sets.

## Select a project

- Run the bundled [collector](scripts/collect_evolve_cases.py) with `uv run --offline --no-project --no-config` and the absolute script path.
- Run from the target Git project or pass `--project-root`; explicitly provide a root for non-Git projects.
- Use the reported `project_id` or supply a stable `--project-id` to match an existing optimizer dataset.
- Use `--previous-root` with an explicitly approved missing path and the existing project ID after moving a project.
- The input defaults to `~/.pi/agent/sessions/`; use `--sessions` only for a user-specified local source.
- Choose one `--benchmark-id` and one target `--skill` for drafting and import.

## Preview, draft, and import

1. Run `scan` to list eligible session and message IDs without printing conversation text.
   It checks the last 30 days by file modification and processes at most 100 in-scope sessions by default.
   A listed next user message is potential feedback, not proof of a failure.
2. Let the user choose requests from their own Pi history, and run `draft --session ID --request ENTRY --benchmark-id BENCHMARK --skill SKILL`.
   Repeat `--request` for multiple entries from the same session.
   If it has multiple branches, ask for the leaf from the scan; pass `--leaf ID` without `--request` to preview that branch's IDs.
3. Give the user the private draft path for local review.
   Never read the draft or original sessions into the model, and never send them through an external service or put their text in tool output.
   Have the user replace private details, minimize the input, and fill each chosen case's `expected` with an observable outcome or pass condition.
   Prefer explicit corrections or directly verified successes; do not use a historical response as the answer key.
4. Import only when the user approves specific case IDs from the reviewed file.
   Use `import --draft PATH --sha256 HASH --case ID --benchmark-id BENCHMARK --skill SKILL`, repeating `--case` as needed.
   Have the user provide the reviewed digest (for example, from `shasum -a 256 PATH`); do not approve on their behalf.
   Report the output path, added IDs, and backup path, not conversation content.

The collector writes `~/.agents/sim/<project-id>/evals/<benchmark-id>/evolve/evolve.json` and a local source index beside the `evolve/` directory.
The optimizer must still verify the baseline on these cases before using them to select edits.
