---
name: use-jira-cli
description: Inspect Jira or prepare and perform precisely authorized Jira mutations with ankitpokhrel/jira-cli (`jira`), including issues, comments, worklogs, epics, sprints, releases, projects, boards, and script-friendly output.
---

# Using Jira CLI

Use read-only discovery freely. Jira creates, edits, transitions, assignments, comments, worklogs, links, sprint/epic changes, and deletes are external writes and require authorization for the exact operation, target, and content. Supplying values for a draft does not authorize execution.

## Establish Context

1. Check `command -v jira`, `jira version`, and `jira me` without exposing token values.
2. Identify the Jira instance and config file before querying or mutating. For multiple configs, use the confirmed `JIRA_CONFIG_FILE` or `-c` path consistently.
3. If setup is missing, do not run interactive `jira init` in an agent shell. Ask the user to complete it or follow a verified non-interactive setup path. Use `JIRA_API_TOKEN`, `.netrc`, keychain, or existing secure configuration; never print, persist, or place secrets in command arguments.
4. Read installed help for version-sensitive syntax: `jira --help`, then `jira <resource> <command> --help`.

## Read Workflow

- Discover project, board, user, status, field, or sprint context before assuming names or IDs.
- Use explicit issue keys for detail views.
- Prefer non-interactive, script-friendly output only when the installed command supports it: `--plain`, `--raw`, `--csv`, `--no-headers`, or `--columns`.
- Avoid commands that open an interactive issue browser; add the supported plain/raw form or use a narrower view.

Read `references/commands.md` only for the relevant resource's common command shapes, then verify flags against installed help.

## Mutation Workflow

1. Read the current target and discover valid field/status values.
2. Prepare the exact Jira instance/config, issue or container IDs, operation, summary/body/comment/worklog text, transition, assignment, and other changed fields. Do not impose a project-name summary prefix or description template unless the user or repository requires it.
3. If the exact operation, target, and content have not already been explicitly authorized for execution, show the complete mutation and ask for approval. Treat requests to draft, explain, review, or prepare Jira content as read-only. Always require exact approval for deletion.
4. After approval, use non-interactive flags only when every required parameter is known. Quote values and provide long content through a template or stdin rather than unsafe shell interpolation.
5. Re-read the affected issue or resource and report its resulting key, status, assignee, fields, or comment/worklog evidence. A zero exit code alone is not sufficient verification.

Do not broaden one approved mutation into related edits. If Jira returns an unexpected prompt, target, schema, or permission requirement, stop without guessing.
