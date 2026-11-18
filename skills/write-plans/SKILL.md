---
name: write-plans
description: Draft, revise, or track implementation plan files for non-trivial work with sequencing, tradeoffs, unknowns, or risks, including completion evidence, external handoff, and completed-plan cleanup; use execute-plans for implementation-to-PR delivery and write-roadmap for strategy.
---

# Writing Plans

This skill owns plan authoring, progress tracking, handoff, and cleanup, not implementation.
For a request to execute a plan, use `execute-plans`, which opens a PR by default after required local checks pass.
Do not infer implementation or publication permission from a request to draft, revise, or track a plan.

Save a drafted plan to a file unless the user requests chat-only output.
Default to `~/.agents/plans/<repo>/` in the user's home directory and update the plan in place during authorized execution.
`<repo>` is the basename of the repository root directory.
Use `<type>_<scope>_<topic>.md`, where `type` describes the work, such as `feat`, `fix`, `refactor`, or `docs`.
The scope is optional; use a module, package, or skill name when useful, or omit it and use `<type>_<topic>.md`.
Do not use placeholder scopes such as `general` or `misc`.
Separate fields with underscores and use concise lowercase kebab-case within each field; do not include dates in the filename.

## Plan Content

Below the plan title, include `Created: YYYY-MM-DD` and `Updated: YYYY-MM-DD`, each on its own line.
Set both fields to the current local date when creating the plan.
Keep `Created` unchanged and set `Updated` to the current local date whenever the plan changes.

Ground the plan in relevant repository evidence and state assumptions or unknowns only when they affect execution or validation.
Always include `Goal`, `Plan`, and `Completion Checklist`.
Add only useful optional sections: `Context`; `Architecture` for system boundaries, ownership, data flow, APIs, state, permissions, storage, or deployment; `Tech Stack` for tool, runtime, or package choices; `Non-Goals`; `Assumptions`; `Unknowns`; and `Risks`.
Include `Rollback / Recovery` for production data, migrations, infrastructure, releases, or public APIs.

## Tasks

Use dependency-ordered Markdown checkboxes that each name one action, its object, expected result, and acceptance evidence.
Limit tasks and finite completion checks to work the agent can perform with available tools, safely prepared dependencies, and granted authorization.
Keep checks in scope when the agent can safely prepare their environment; do not classify work by test type alone.
Turn material unknowns into early discovery tasks.
Keep dependent tasks blocked when a missing external prerequisite prevents safe implementation.

## External Handoff

When work cannot be performed by the agent, record it without completion checkboxes in an optional `External Handoff` section instead of making it an agent task or completion check.
This includes human-operated physical-device tests, subjective visual or usability acceptance, unavailable platform or native UI checks, account-owner actions such as MFA and credential setup, unauthorized external or costly operations, and external approvals or upstream dependencies.
Create agent tasks to prepare available evidence, such as before/after captures for visual review, and the handoff, not to wait for another actor.
For each external item, name the responsible role, prerequisite, action, expected result, unverified behavior, and any release restriction.
Do not require user acceptance merely to close the coding plan; preserve acceptance requirements explicitly imposed by the user or higher-priority instructions, even when they block completion.
External handoff does not authorize external writes, costly operations, or requests for secrets in chat.

## Tracking and Completion

While tracking authorized implementation:

- Check a task only after its acceptance method passes, adding concise evidence when completion is not obvious from repository state.
- Leave failed or unavailable agent checks open; use External Handoff only for work outside the agent's capabilities or authorization.
- Mark genuinely inapplicable tasks as `- [x] Not applicable: <reason>` and reopen tasks whose evidence is invalidated; lack of access is not evidence that a check passed or is inapplicable.
- Keep change-caused failures and unresolved implementation correctness or safety questions blocking; an unavailable external check alone is not evidence of an implementation defect.
- For unrelated baseline failures, record evidence and follow repository policy without waiving mandatory gates on your own.
- Track only the current saved plan without inspecting or altering unrelated plans; for a chat-only plan, show updated checkboxes and evidence in chat.

Declare agent-plan completion only when every task and completion check has valid evidence, required gates pass or have an authorized exception, material unknowns and risks have a clear disposition, and external handoff preparation is complete.
Agent-plan completion does not establish product acceptance or release readiness.
Before deleting a completed saved plan, preserve unresolved external items in an appropriate retained repository document, using an existing acceptance or operations document when suitable, or in an explicitly requested chat-only handoff.
Do not require a new file or external issue for every plan, or write to an external tracker without authorization.
Report verified work, unverified external checks, release restrictions, and the retained handoff location when applicable.
Only then delete the completed saved plan and report its path; never delete a chat-only plan or one with missing completion evidence.
