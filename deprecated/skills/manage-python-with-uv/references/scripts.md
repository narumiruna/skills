# Standalone Scripts with uv

Use these patterns for a script that should not become a shared project. Prefer inline metadata for reusable files and `--with` for disposable invocations.

## Run and Isolate

```bash
uv run example.py arg1
uv run --with rich example.py
uv run --with rich --with requests example.py
```

Inside a project, `uv run` can use the project environment. Add `--no-project` before the script only when it must ignore that environment and does not import local package code:

```bash
uv run --no-project example.py
```

Inline script metadata isolates dependencies automatically.

For stdin or a heredoc:

```bash
echo 'print("hello")' | uv run --no-project -
uv run --no-project - <<'PY'
print("hello")
PY
```

## Inline Metadata

```bash
uv init --script example.py --python 3.12
uv add --script example.py 'requests<3' rich
```

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests<3", "rich"]
# ///
```

Use an empty `dependencies = []` when no packages are needed. Carry a Python requirement in metadata for reusable scripts; use `uv run --python <version>` for an ad hoc override.

## Executable Script

```python
#!/usr/bin/env -S uv run --script

print("Hello")
```

Make it executable only when the target platform and repository expect a shebang workflow.

## Reproducibility

Create a neighboring lockfile when reproducible resolution matters:

```bash
uv lock --script example.py
```

Use `exclude-newer` in `[tool.uv]` metadata only when the workflow requires a resolution cutoff. Commit the lockfile when the script and repository policy treat it as source.

## Alternate Index

Use an alternate index only when authorized and avoid embedding credentials:

```bash
uv add --index "https://example.com/simple" --script example.py requests
```

Review the resulting metadata and trust policy before sharing the script.

## Platform Notes

- Windows `.pyw` files run with the GUI interpreter through `uv run example.pyw`.
- Inline dependencies continue to apply on supported platforms.
- Verify shebang and shell quoting on the actual target platform rather than assuming POSIX behavior.
