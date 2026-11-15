# Quality Workflows with uv

Prefer the repository's documented aggregate gate. Do not add or replace quality tools merely to run validation.

## Existing Repositories

1. Inspect project instructions, `pyproject.toml`, hook configuration, and CI.
2. Run the narrowest relevant check while iterating.
3. Run the documented full gate before handoff.
4. Use the configured hook runner. If the repository uses prek, run `prek run -a`; if it uses pre-commit instead, run its documented command.

Typical direct commands when the corresponding tools are already configured:

```bash
uv run ruff check
uv run ruff format --check
uv run ty check
uv run pytest tests
uv run pytest --cov=<package-or-src-path> --cov-report=term-missing tests
```

Use project-specific targets and thresholds when defined. Do not invent a coverage threshold or assume `tests/` when repository evidence points elsewhere.

## New Projects

When no project requirements exist, choose the smallest tool set that proves the requested quality bar. Common options are:

```bash
uv add --dev pytest ruff ty
```

Add coverage or a hook runner only when the workflow needs it. Prefer function-based pytest tests with plain `assert`, fixtures for lifecycle setup, and parametrization for input matrices, unless the project has another established style.

## Handoff

Report the commands run and their outcomes. Distinguish passing checks from checks that were unavailable or intentionally not configured.
