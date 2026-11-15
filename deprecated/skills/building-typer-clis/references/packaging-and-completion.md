# Typer Packaging and Completion

Load this reference when adding Typer, wiring an executable, supporting `python -m`, testing a wheel, enabling completion, or migrating across Typer versions.

## Use the Current Package

Inspect the project's Python range, existing Typer constraint, and lockfile before changing dependencies. Add plain Typer through the repository workflow with `uv add typer`.

Do not add `typer[all]`, `typer-slim`, or `typer-cli` to a current project. Plain `typer` includes Rich, shellingham, and the `typer` command; the slim and CLI distributions stopped receiving releases and now defer to `typer`.

Do not silently raise the minimum Python version or upgrade a pinned Typer release. When a migration is requested, read the release notes between the current and target versions and test command grammar, help, completion, and runner behavior.

## Wire Each Supported Invocation Explicitly

For an installed executable, point `[project.scripts]` at the explicit app:

```toml
[project.scripts]
my-command = "my_package.cli:app"
```

The left side is the executable users call. The right side is the importable module and `typer.Typer()` object. An installed entry point does not require an `if __name__ == "__main__"` block.

For direct script execution, use a guard:

```python
if __name__ == "__main__":
    app()
```

For optional `python -m my_package` support, add `my_package/__main__.py`:

```python
from .cli import app

app()
```

These are separate public invocation modes. Test every mode the project documents instead of assuming that an importable app proves the script metadata or module path.

## Build and Test the Distribution

Use the repository's uv workflow. For a package, representative checks are:

```bash
uv sync
uv run my-command --help
uv build
uv tool run --from path/to/dist/package-version-py3-none-any.whl my-command --help
```

Choose the actual artifact path produced by the build. `uv tool run --from` uses an isolated tool environment instead of overwriting an unrelated installed command. Publishing is a separate external action; use the dedicated uv packaging workflow and require exact publication authorization.

## Preserve Completion

Shell completion is tied to a stable installed executable name. It does not work through `python -m my_package`. When completion is required:

- install and invoke the `[project.scripts]` command
- exercise `--show-completion` or the relevant shell in a disposable environment before claiming it works
- keep imports, app construction, callbacks, and custom `autocompletion` functions fast and free of stdout diagnostics or external side effects
- remember that completion executes the program with protocol environment variables

Do not install completion into the user's shell merely to test command wiring. That mutates external configuration and requires explicit authorization.

## Treat Version Boundaries as Compatibility Work

Typer 0.26.0 vendors Click. For current Typer, do not extract a Click application, attach Click plug-ins, subclass Click's runner, or depend on Click-specific internals. Prefer documented Typer parameters and APIs; several inherited settings are compatibility-only or deprecated.

Other migration-sensitive surfaces include:

- explicit names for `add_typer()` groups
- `Annotated` parameter declarations
- `shell_complete` versus Typer's `autocompletion`
- `mix_stderr` and the current Typer `CliRunner`
- exact Rich help and metavar rendering
- Python-version support

Pin versions when exact rendering is a product requirement; otherwise assert semantic help content.

## Official Sources

- [Install Typer](https://typer.tiangolo.com/tutorial/install/)
- [Building a Package](https://typer.tiangolo.com/tutorial/package/)
- [Features: shell completion](https://typer.tiangolo.com/features/)
- [Release Notes](https://typer.tiangolo.com/release-notes/)
- [Vendored Click](https://typer.tiangolo.com/tutorial/click/)
