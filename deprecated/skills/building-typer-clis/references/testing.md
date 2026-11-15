# Testing Typer CLIs

Load this reference when adding or revising CLI tests. Test business behavior directly and use `typer.testing.CliRunner` for the Typer boundary.

## Test the Public Grammar

The argument list passed to `runner.invoke()` starts after the executable name. Match the real command shape:

```python
from typer.testing import CliRunner

from my_package.cli import app

runner = CliRunner()


def test_import_requires_existing_file(tmp_path) -> None:
    source = tmp_path / "records.json"
    source.write_text("[]")

    result = runner.invoke(app, [str(source), "--limit", "10"])

    assert result.exit_code == 0
    assert "Imported 0 records" in result.stdout
```

For a one-command app, do not insert the function name. For a grouped app, include each public command or group. Add a regression test before introducing a second command or application callback because that can change the entire invocation grammar.

## Cover Observable Boundaries

Exercise representative cases:

- success with converted values
- missing, malformed, bounded, and callback-invalid parameters
- deliberate zero and nonzero `typer.Exit` paths
- aborted confirmation or interaction
- prompt input with `input="value\n"`
- environment fallback with `env={"NAME": "value"}`
- filesystem effects in a pytest `tmp_path`
- stable `--help` fragments, command names, option names, and required/default semantics

Assert `result.exit_code` first. Use `result.stdout` and `result.stderr` when the stream matters; `result.output` is useful when combined terminal output is the contract. Avoid snapshots of complete Rich help or metavar spacing unless exact rendering is itself required and the Typer version is pinned.

Use `catch_exceptions=False` temporarily when diagnosing an unexpected exception. Do not make a passing test depend on a traceback for an expected user error.

## Respect Current Runner Boundaries

Typer's testing surface changed across versions. Inspect the declared Typer version rather than copying old Click examples.

For current Typer 0.26+:

- `CliRunner` is Typer's runner, not the public Click runner.
- Do not pass `mix_stderr`; current results expose stdout and stderr separately.
- Do not assume `isolated_filesystem()` exists. Use pytest `tmp_path` and `monkeypatch.chdir(tmp_path)` when a current-working-directory boundary matters.
- Invoke runners sequentially. Runner calls replace process-global streams and environment during execution and are not a safe concurrent-test primitive.
- Do not rely on Click plug-ins, runner subclasses, or undocumented Click internals.

For an older pinned Typer version, consult its matching release notes and runner signature. Do not silently upgrade merely to make a copied test helper work.

## Separate CLI and Domain Tests

A CLI test should prove parsing, help, rendering, and exit behavior. It should not need real network calls, publication, destructive mutations, wall-clock time, randomness, or persistent user configuration.

Inject or mock those effects and test the ordinary function underneath directly. Keep at least one boundary test proving that the command translates a known domain result or failure into the intended message and exit code.

When packaging is in scope, add a subprocess smoke test for the installed `[project.scripts]` executable or isolated wheel in addition to `CliRunner`; importing `app` does not prove distribution metadata works.

## Official Sources

- [Testing](https://typer.tiangolo.com/tutorial/testing/)
- [Building a Package](https://typer.tiangolo.com/tutorial/package/)
- [Release notes: `mix_stderr` removal](https://typer.tiangolo.com/release-notes/#0160-2025-05-26)
- [Release notes: vendored Click](https://typer.tiangolo.com/release-notes/#0260-2026-05-26)
- [Vendored Click](https://typer.tiangolo.com/tutorial/click/)
