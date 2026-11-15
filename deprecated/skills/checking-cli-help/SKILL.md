---
name: checking-cli-help
description: Decide whether to inspect command help before execution when the exact subcommand, flags, targets, side effects, or help mechanism are uncertain.
metadata:
  internal: true
---

# Checking CLI Help (Deprecated Reference)

Run a command directly only when you can explain its exact target, effect, and material flags. Otherwise inspect the narrowest relevant help first.

Use this order as applicable:

1. `<cmd> <subcommand> --help`
2. `<cmd> --help` or the tool's built-in `help` form
3. `type <cmd>` or `command -v <cmd>` to identify aliases, functions, or builtins
4. shell `help <builtin>`
5. `man <cmd>` when non-interactive access is available

Judge familiarity on the full command, not a whitelist or the base executable name. Help output does not authorize an external, destructive, costly, or otherwise unapproved action; it only resolves syntax and behavior.
