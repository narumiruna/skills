---
name: building-codex-hooks
description: Design, implement, review, or debug the deprecated repository reference for Codex CLI hooks, including hooks.json layers, event matchers, stdin/stdout contracts, and hook scripts. Verify current Codex documentation before relying on version-sensitive behavior.
metadata:
  internal: true
---

# Codex CLI Hooks (Deprecated Reference)

Treat bundled runtime details as historical until checked against the installed Codex version and current official documentation. Hooks are workflow guardrails, not a security boundary.

## Workflow

1. Verify that hooks, event names, feature flags, config locations, and platform support still exist in the current runtime.
2. Choose the personal or repository config layer deliberately. Determine whether matching hooks compose or override from current documentation.
3. Select one event and implement the smallest valid handler before adding matchers, policy logic, file I/O, or transcript parsing.
4. Resolve repository-local commands from the Git root rather than assuming session `cwd`.
5. Use a custom script when payload inspection or event-specific JSON is required. Use a command wrapper only when current docs support it and exit-status mapping is sufficient.
6. Validate stdin and stdout against the chosen event contract, then test single and multiple matching hooks and the failure path.

Read `references/events.md` for the recorded event matrix and `references/examples.md` for minimal historical examples, but reverify every field and output shape before implementation.

## Design Rules

- Keep config small and group one matcher intent at a time.
- Treat payload fields as untrusted and unsupported fields as fail-open.
- Pass commands as argv rather than a concatenated shell string.
- Expect concurrent execution only if the current runtime documents it.
- A post-tool hook cannot undo an effect that already occurred.
- Do not describe partial shell/tool interception as complete enforcement.

## Handoff

Report the runtime/docs version checked, config layer, event and matcher, handler artifact, contract tests, and any unsupported or fail-open path. Do not publish, install user-global hooks, or enable repository policy externally unless requested.
