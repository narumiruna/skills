# Typer Application Architecture

Load this reference when commands, callbacks, context, nested groups, or help behavior could change the public CLI grammar.

## Preserve Command Shape

An explicit `typer.Typer()` app is extensible and directly testable. Prefer it to `typer.run()` for production CLIs.

Typer treats these shapes differently:

- With exactly one registered `@app.command()`, that function is promoted to the root: `PROGRAM [ARGS]...`. Its Python function name is not a subcommand.
- With multiple registered commands, the grammar becomes `PROGRAM COMMAND [ARGS]...`.
- Registering any sub-app also creates grouped grammar, even if the root previously had one promoted command.
- Adding an application callback also makes the registered command explicit, even when only one command exists.

Adding a second command, registering a sub-app, or adding a callback can therefore break scripts that previously called `PROGRAM VALUE`. Before changing shape, inventory documentation, shell scripts, CI, completion, and tests. Either preserve compatibility or report the migration explicitly.

Use explicit apps even for one command when extension or installed entry points are likely:

```python
import typer

app = typer.Typer()


@app.command()
def main(name: str) -> None:
    print(f"Hello {name}")
```

This is invoked as `program Ada`, not `program main Ada`.

## Compose Named Groups

Create one root app and separate sub-apps by responsibility. Register every group with an explicit public name:

```python
import typer

app = typer.Typer()
users_app = typer.Typer()


@users_app.command()
def create(name: str) -> None:
    print(f"Creating {name}")


app.add_typer(users_app, name="users")
```

The command is `program users create Ada`. Do not infer a group's name from its callback; Typer removed that behavior. Keep nesting only when it matches a real user-facing hierarchy.

## Use Callbacks Deliberately

An application callback owns options that appear before the subcommand:

```text
program --verbose users create Ada
```

The same option after `users create` belongs to that command and is not a root option. A callback also runs before the selected command, so avoid expensive or side-effecting initialization when help, completion, or a narrower command does not need it.

For a default root action alongside subcommands:

```python
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        print("Default action")
```

For a current grouped Typer app, choose the no-command behavior explicitly: the default missing-command error rejects an omitted command, `no_args_is_help=True` shows help, and `invoke_without_command=True` runs the callback as a default action. Inspect older pinned versions before changing this behavior.

A callback docstring can provide root help, but adding a callback solely for documentation still changes a one-command app into a command group. Treat that as a grammar decision, not harmless decoration.

## Help and Naming

- Keep public command and option names stable; Python underscores normally become CLI dashes.
- Give `add_typer()` groups explicit names and meaningful help.
- Use stable semantic help assertions. Rich formatting and metavar layout can change across Typer versions.
- Keep pass-through `context_settings` such as `allow_extra_args` and `ignore_unknown_options` for deliberate wrapper CLIs; they bypass normal typed parsing.

## Official Sources

- [One or Multiple Commands](https://typer.tiangolo.com/tutorial/commands/one-or-multiple/)
- [Typer Callback](https://typer.tiangolo.com/tutorial/commands/callback/)
- [Using the Context](https://typer.tiangolo.com/tutorial/commands/context/)
- [Add Typer](https://typer.tiangolo.com/tutorial/subcommands/add-typer/)
- [Release notes: explicit group naming](https://typer.tiangolo.com/release-notes/#0140-2024-11-28)
