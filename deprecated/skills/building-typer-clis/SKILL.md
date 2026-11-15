---
name: building-typer-clis
description: Deprecated internal reference for building, extending, packaging, migrating, or testing Python CLIs with Typer, including command grammar, typed parameters, callbacks, completion, entry points, and CliRunner behavior.
metadata:
  internal: true
---

# Building Typer CLIs (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility. Preserve the public invocation grammar while keeping Typer commands as thin adapters between typed terminal input and ordinary Python functions.

## Load Focused Guidance

| Need | Read |
| --- | --- |
| Single versus multiple commands, callbacks, context, groups, or help | `references/application-architecture.md` |
| `typing.Annotated`, defaults, parameter types, prompts, validation, exits, or value completion | `references/parameters-and-runtime.md` |
| `CliRunner`, input, streams, files, errors, help, or entry-point tests | `references/testing.md` |
| Dependency choice, installed commands, `python -m`, wheels, shell completion, or Typer migration | `references/packaging-and-completion.md` |

## Workflow

1. Inspect `pyproject.toml`, the declared Typer version and Python range, existing invocation examples, entry points, app/callback structure, tests, and repository commands. Do not silently upgrade Typer or redesign the CLI.
2. Preserve command shape deliberately. Typer promotes one registered command to the root grammar, `PROGRAM [ARGS]...`; adding a second command, registering a sub-app with `app.add_typer(...)`, or adding an application callback changes it to `PROGRAM COMMAND [ARGS]...`. Treat that transition, command renames, option renames, and moved root options as public-interface changes.
3. Use one explicit root `typer.Typer()` app. Compose domain groups with explicit `app.add_typer(sub_app, name="...")` names and use an application callback only for genuine root options, initialization, documentation, or a deliberate default action.
4. Prefer `typing.Annotated` with `typer.Argument()` and `typer.Option()`. Put static defaults in Python assignments, use `default_factory=` for dynamic defaults, and let Typer perform supported type conversion and boundary validation.
5. Keep command bodies thin. Use `typer.BadParameter` for parameter-specific validation, `typer.Exit` for deliberate termination and exit status, and `typer.Abort` for an aborted interaction. Translate domain failures at the CLI boundary without exposing tracebacks by default.
6. Keep parameter callbacks and autocompletion fast, side-effect-free, and silent on stdout. When callback work must be skipped during completion, check `ctx.resilient_parsing` before validation or output.
7. Wire only the invocation modes the project supports: a guarded `app()` for direct scripts, `[project.scripts]` for installed commands, and package `__main__.py` for `python -m package`. Exercise the actual installed command when packaging or shell completion is in scope.
8. Test the current public grammar, typed parsing, success, validation failure, deliberate exits, prompts, stable help fragments, and any filesystem or environment boundary with `typer.testing.CliRunner`; test business logic directly.

## Constraints

- Add plain `typer` through the repository's uv workflow only when missing; do not introduce obsolete Typer packages or extras.
- Preserve non-interactive use when adding prompts. Keep secrets out of argv where practical, and distinguish value re-entry from affirmative consent for a destructive action.
- Mock or inject external, destructive, costly, or nondeterministic effects in CLI tests.
- Inspect release notes before relying on Click integration, exact Rich help rendering, runner internals, or another version-sensitive surface.

Finish with the supported invocation forms exercised, behavior and exit codes covered, packaging checked when applicable, and exact validation evidence reported.
