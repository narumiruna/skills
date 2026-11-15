# Typer Parameters and Runtime Behavior

Load this reference for nontrivial arguments, options, prompts, callbacks, completion, or error and exit behavior.

## Declare Parameters with `Annotated`

Prefer `typing.Annotated`; the older style that stores `typer.Argument(...)` or `typer.Option(...)` as the Python default is deprecated.

```python
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer()


@app.command()
def import_data(
    source: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    limit: Annotated[int, typer.Option(min=1)] = 100,
) -> None:
    ...
```

Parameter requiredness comes from the presence of a default value:

- The absence of both a Python assignment and `default_factory=` means required, including for an option.
- An assignment supplies a static default and makes the parameter optional.
- `default_factory=` inside `Argument()` or `Option()` supplies a dynamic default and also makes the parameter optional.
- Do not combine `default_factory=` with a Python assignment; Typer rejects two defaults.
- `T | None` describes an accepted value; it does not by itself make a parameter optional.

Prefer Typer's supported types and constraints before custom parsing:

- `Enum` or `Literal` for choices.
- `Path` with `exists`, `file_okay`, `dir_okay`, `readable`, `writable`, or `resolve_path` when those checks match the contract.
- `list[T]` for repeated values; repeated options are supplied by repeating the flag.
- Fixed tuples for fixed-arity values.
- `datetime` with explicit `formats=` when the accepted format is part of the interface.
- `typer.FileText` or `typer.FileBinaryRead` only when passing open file objects is preferable to a `Path` boundary.

Do not assume paths expand `~`, datetimes accept every ISO-8601 form, or list and tuple parameters share the same grammar. Exercise the actual accepted forms.

## Validate and Terminate at the Boundary

Use a parameter callback when validation belongs to one argument or option:

```python
def positive(value: int) -> int:
    if value <= 0:
        raise typer.BadParameter("must be greater than zero")
    return value
```

`typer.BadParameter` associates the failure with the originating parameter and renders usage. Use ordinary domain exceptions inside business logic and translate them once at the command boundary.

Use the termination types deliberately:

- `raise typer.Exit()` for an intentional successful early stop.
- `raise typer.Exit(code=n)` for a deliberate nonzero status after rendering the intended message.
- `raise typer.Abort()` for an aborted interaction; Typer renders `Aborted!`.

Do not use `BadParameter` for an unrelated service or business failure merely to obtain formatted output.

## Prompts, Secrets, and Consent

`prompt=True` asks only when an option is omitted. Preserve a non-interactive flag or environment path for automation.

For secrets, `hide_input=True` hides interactive typing and `confirmation_prompt=True` asks for the same value twice. They do not protect a value supplied directly in argv, which may be visible in shell history or process listings. Prefer a secure prompt, environment variable, file, or existing secret provider according to the application's threat model.

`confirmation_prompt=True` confirms equality, not user intent. For an affirmative destructive-action decision, use a separate confirmation such as:

```python
typer.confirm("Delete all cached records?", abort=True)
```

Keep destructive execution outside tests or inject the effect.

## Callbacks and Completion

A parameter callback and an `autocompletion` function can receive typed injected values such as `typer.Context`; completion functions can also receive the incomplete `str` and raw `list[str]` arguments.

- Use `autocompletion=...` for custom value completion. The inherited `shell_complete` parameter is deprecated and not fully functional.
- Return or yield strings, or `(value, help)` tuples where the shell supports help text.
- Filter on the incomplete value and keep completion bounded, fast, and deterministic.
- Never print normal diagnostics to stdout during completion; completion reads stdout as its protocol.
- Parameter callbacks may execute during completion. Check `ctx.resilient_parsing` and return before validation, output, network, or storage work when it is true.
- Root import and app construction must also avoid side effects because completion starts the program.

## Official Sources

- [Parameters reference](https://typer.tiangolo.com/reference/parameters/)
- [CLI Option Callback and Context](https://typer.tiangolo.com/tutorial/options/callback-and-context/)
- [CLI Option autocompletion](https://typer.tiangolo.com/tutorial/options-autocompletion/)
- [Password and Confirmation Prompt](https://typer.tiangolo.com/tutorial/options/password/)
- [Terminating](https://typer.tiangolo.com/tutorial/terminating/)
- [Parameter Types](https://typer.tiangolo.com/tutorial/parameter-types/)
- [Multiple Values](https://typer.tiangolo.com/tutorial/multiple-values/)
