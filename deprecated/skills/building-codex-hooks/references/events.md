# Event Reference

> Deprecated, version-sensitive snapshot. Verify every event, field, matcher, and output contract against the installed Codex version and current official documentation before use.

Use this file only when historical event differences help interpret or migrate an existing hook.

## Common Inputs

Every hook command receives one JSON object on `stdin`.

| Field | Type | Meaning |
| --- | --- | --- |
| `session_id` | `string` | Current session or thread id |
| `transcript_path` | `string \| null` | Session transcript path, if any |
| `cwd` | `string` | Session working directory |
| `hook_event_name` | `string` | Current hook event |
| `model` | `string` | Active model slug |

Turn-scoped events also provide `turn_id`.

## SessionStart

- Matcher applies to `source`
- Current sources: `startup`, `resume`
- Plain text on `stdout`: added as extra developer context
- JSON on `stdout`: common output fields plus:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Load the workspace conventions before editing."
  }
}
```

## PreToolUse

- Matcher applies to `tool_name`
- Current `tool_name`: `Bash`
- Extra inputs:
  - `tool_use_id`
  - `tool_input.command`
- Plain text on `stdout`: ignored
- Supported structured behavior:
  - `systemMessage`
  - deny with:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook."
  }
}
```

- Legacy block shape also works:

```json
{
  "decision": "block",
  "reason": "Destructive command blocked by hook."
}
```

- Exit code `2` with `stderr` also blocks
- Important fail-open note:
  `allow`, `ask`, `updatedInput`, `additionalContext`, `continue: false`, `stopReason`, and `suppressOutput` are parsed but not supported yet

## PostToolUse

- Matcher applies to `tool_name`
- Current `tool_name`: `Bash`
- Extra inputs:
  - `tool_use_id`
  - `tool_input.command`
  - `tool_response`
- Plain text on `stdout`: ignored
- Structured review shape:

```json
{
  "decision": "block",
  "reason": "The Bash output needs review before continuing.",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "The command updated generated files."
  }
}
```

- `decision: "block"` does not undo the command; it replaces the tool result with feedback and continues
- Exit code `2` with `stderr` also injects feedback
- `continue: false` is supported here
- `updatedMCPToolOutput` and `suppressOutput` are parsed but not supported

## UserPromptSubmit

- Matcher is ignored
- Extra input:
  - `prompt`
- Plain text on `stdout`: added as extra developer context
- JSON on `stdout`: common output fields plus:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "Ask for a clearer reproduction before editing files."
  }
}
```

- To block:

```json
{
  "decision": "block",
  "reason": "Ask for confirmation before doing that."
}
```

## Stop

- Matcher is ignored
- Extra inputs:
  - `stop_hook_active`
  - `last_assistant_message`
- `stdout` must be JSON when exit code is `0`
- To continue for one more pass:

```json
{
  "decision": "block",
  "reason": "Run one more pass over the failing tests."
}
```

- `decision: "block"` here means continue, not reject
- If any matching `Stop` hook returns `continue: false`, that takes precedence over continuation from other matching `Stop` hooks
