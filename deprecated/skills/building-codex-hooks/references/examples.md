# Minimal Examples

> Deprecated, version-sensitive examples. Verify config paths, events, fields, and output contracts against current Codex documentation before adapting them.

Use these to interpret or migrate an existing hook; expand only after a current minimal contract works.

## SessionStart: add context on startup or resume

`hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 ~/.codex/hooks/session_start.py",
            "statusMessage": "Loading session notes"
          }
        ]
      }
    ]
  }
}
```

`session_start.py`

```python
#!/usr/bin/env python3
import json
import sys

payload = json.load(sys.stdin)
print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"Session started from {payload['source']}."
            }
        }
    )
)
```

## PreToolUse: deny destructive Bash commands

`hooks.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/pre_tool_use.py\"",
            "statusMessage": "Checking Bash command"
          }
        ]
      }
    ]
  }
}
```

`pre_tool_use.py`

```python
#!/usr/bin/env python3
import json
import sys

payload = json.load(sys.stdin)
command = payload["tool_input"]["command"]

if "rm -rf" in command:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Blocked destructive command."
                }
            }
        )
    )
```

## PostToolUse: replace raw tool result with feedback

```python
#!/usr/bin/env python3
import json
import sys

payload = json.load(sys.stdin)
command = payload["tool_input"]["command"]

if command.startswith("git add "):
    print(
        json.dumps(
            {
                "decision": "block",
                "reason": "Review staged paths before continuing.",
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": "Confirm staging scope is intentional."
                }
            }
        )
    )
```

## UserPromptSubmit: ask for safer framing

```python
#!/usr/bin/env python3
import json
import sys

payload = json.load(sys.stdin)

if "production database" in payload["prompt"].lower():
    print(json.dumps({"decision": "block", "reason": "Ask for explicit confirmation first."}))
```

## Stop: wrap an existing validation command with `codhc`

`hooks.json`

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uvx codhc ruff check --fix",
            "statusMessage": "Running Ruff fixes",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

Use this pattern when the hook only needs to run an existing command and turn its exit status into a valid `Stop` hook response.

## Stop: custom continuation reason with a script

```python
#!/usr/bin/env python3
import json
import sys

payload = json.load(sys.stdin)
if payload.get("stop_hook_active"):
    print(json.dumps({}))
else:
    print(json.dumps({"decision": "block", "reason": "Run one more pass over failing checks."}))
```

## Practical Notes

- Start with one event per file until behavior is proven.
- Prefer repo-local paths resolved from `git rev-parse --show-toplevel`.
- Prefer `codhc` for simple `Stop` hooks that only wrap an existing check command.
- Prefer a custom script when the hook must inspect the payload or compute its own response text.
- Keep hook output machine-readable; ad hoc logs often make the event look broken.
