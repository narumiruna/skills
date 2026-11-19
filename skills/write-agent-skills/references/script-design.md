# Design scripts for agents

Use an existing tool for a short command with a stable interface.
Bundle a tested script under `scripts/` when agents would otherwise have to reconstruct the same parsing, validation, or transformation on each run.
Keep judgment and decisions about authorization in the skill instructions.

## Define the interface

- Make the script non-interactive and accept input through arguments, environment variables, or standard input.
- Document required runtime versions and dependencies, using the target repository's conventions.
  Pin dependencies when version changes could break the workflow.
- Provide `--help` with expected inputs, one working invocation, and where results go.
- Reject invalid input with a nonzero exit code and an error that says what to fix.
- Send structured results to stdout and diagnostics to stderr when the output is meant for another tool.
  Bound large results or let the caller write them to a file.

## Make runs safe and verifiable

- Prefer read-only defaults and make repeated runs safe where possible.
- Provide a dry run or an explicit acknowledgement flag for state-changing actions as appropriate.
  A command-line flag does not replace user approval.
- In `SKILL.md`, link to the script and show how to invoke it, including the working directory if it matters.
- Before shipping a change, run a realistic input and a failure case without writing to production or other external systems.

See [using scripts in skills](https://agentskills.io/skill-creation/using-scripts).
