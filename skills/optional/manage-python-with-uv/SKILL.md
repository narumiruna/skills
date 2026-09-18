---
name: manage-python-with-uv
description: Manage Python projects and standalone scripts with uv, including setup, dependencies, execution, quality gates, locking, builds, and release preparation. Use for `uv run`, `uv add`, inline script metadata, packaging, or an explicitly requested publish workflow.
---

# Python with uv

Use the repository's existing Python and verification choices first; use uv for dependency and execution operations unless a documented repository command wraps them.

## Choose the Mode

- **Project:** a `pyproject.toml`, lockfile, shared package, or local imports define an environment.
- **Standalone script:** one file or stdin should run without creating a project.
- Use `--no-project` only when the invocation must ignore the surrounding project and does not import its code.

## Project Workflow

1. Inspect `pyproject.toml`, lockfiles, repository instructions, and existing tools.
2. Initialize only genuinely new projects with `uv init`. Add or remove dependencies with `uv add` and `uv remove`; use `uv sync` to reconcile declared state.
3. Run Python and project tools through `uv run` or the repository's documented wrapper.
4. Preserve the established test, lint, type-check, coverage, and hook stack. For a new project with no stated requirements, add only tools that serve the requested quality bar.
5. Update and inspect the lockfile when dependency inputs change.
6. Run the narrow checks needed during iteration, then the repository's aggregate gate.

## Standalone Script Workflow

1. Use `uv run script.py` when no extra dependency is needed.
2. Use `uv run --with <dependency> script.py` for disposable dependencies.
3. Use `uv init --script` and `uv add --script` when dependencies or Python requirements should travel with a reusable script.
4. Put `--no-project` before the script name when isolation is intentional.
5. Read `references/scripts.md` only for inline metadata, stdin, shebang, locking, alternate indexes, or platform-specific patterns.

## Quality and Release

Use verification in this order: documented aggregate gate; the repository's configured hook runner; individual `uv run ...` commands when no aggregate gate exists or when narrowing a failure. Do not introduce or switch tools solely to run checks. Read `references/quality.md` for fallback patterns.

For release preparation:

1. Run the repository gate.
2. Build with `uv build --no-sources` so local source overrides cannot leak.
3. Inspect wheel and sdist contents.
4. Install and test the built wheel in a fresh uv-managed invocation.
5. Record the artifact names, checks, and lockfile state.

Publishing is a separate external write. Do not run `uv publish` based only on a request to build, package, prepare, or release. Require authorization for the exact package/version, repository or index, and artifacts; use secret-safe credentials and verify the resulting release. Read `references/packaging.md` for the authorized publish path.

## Invariants

- Do not use `pip install` to mutate a uv-managed project.
- Do not create `pyproject.toml` merely to run a one-file script.
- Do not use `--no-project` when local project imports are required.
- Treat `--with` as ephemeral; encode dependencies when reuse or reproducibility matters.
- Test the built or published artifact, not only the source checkout.
