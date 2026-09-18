---
name: write-plans
description: Draft, execute, or track lean, verifiable implementation plans for non-trivial migrations, refactors, PR splits, task checklists, and other work with sequencing, tradeoffs, unknowns, or risks, and delete them when complete; use write-roadmap for strategic direction and skip small obvious tasks.
---

# Writing Plans

Save a drafted plan to the repository unless the user requests chat-only output.
Default to `docs/plans/YYYY-MM-DD_<topic>-plan.md` with a concise lowercase kebab-case topic and update it in place during authorized execution.

## Plan Content

Ground the plan in relevant repository evidence and state assumptions or unknowns only when they affect execution or validation.
Always include `Goal`, `Plan`, and `Completion Checklist`.
Add only useful optional sections: `Context`; `Architecture` for system boundaries, ownership, data flow, APIs, state, permissions, storage, or deployment; `Tech Stack` for tool, runtime, or package choices; `Non-Goals`; `Assumptions`; `Unknowns`; and `Risks`.
Include `Rollback / Recovery` for production data, migrations, infrastructure, releases, or public APIs.

## Tasks

Use dependency-ordered Markdown checkboxes that each name one action, its object, expected result, and acceptance evidence.
Turn material unknowns into early discovery tasks.
End with finite completion checks tied to files, commands, tests, review or deployment state, or explicit user acceptance.

## Tracking and Completion

During authorized execution:

- Check a task only after its acceptance method passes, adding concise evidence when completion is not obvious from repository state.
- Leave failed or unavailable checks open, mark inapplicable tasks as `- [x] Not applicable: <reason>`, and reopen tasks whose evidence is invalidated.
- Track only the current saved plan without inspecting or altering unrelated plans; for a chat-only plan, show updated checkboxes and evidence in chat.

Declare completion only when every task and completion check is checked, material unknowns are resolved or accepted, risks have a clear disposition, and required handoff or release work is done.
Delete a completed saved plan and report its path only after these conditions are met; never delete a chat-only plan or one with missing completion evidence.
