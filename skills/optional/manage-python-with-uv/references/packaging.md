# Packaging with uv

## Build and Inspect

Run the repository gate, then build release-ready artifacts without local source overrides:

```bash
uv build --no-sources
```

Inspect the actual filenames in `dist/` rather than assuming a version or wheel tag:

```bash
unzip -l dist/<package>-<version>-<tags>.whl
tar -tzf dist/<package>-<version>.tar.gz
```

Check required package data, metadata, licenses, and unexpected files. Test installation from the wheel outside the source checkout:

```bash
uv run --no-project --with dist/<package>-<version>-<tags>.whl \
  python -c "import <import_name>"
```

A `src/` layout can help prevent checkout-only imports but is not required. Diagnose missing files through the build-backend and package-data configuration rather than assuming one layout.

## Publish Boundary

Building or preparing a release does not authorize publication. Before running `uv publish`, confirm the exact package and version, target repository/index, and artifacts. Keep tokens out of arguments and logs; prefer trusted publishing in supported CI.

After exact authorization, publish to the confirmed target:

```bash
UV_PUBLISH_TOKEN="$PYPI_TOKEN" uv publish dist/<authorized-artifacts>
```

For an authorized Test PyPI upload:

```bash
UV_PUBLISH_TOKEN="$TEST_PYPI_TOKEN" \
UV_PUBLISH_URL="https://test.pypi.org/legacy/" \
uv publish dist/<authorized-artifacts>
```

Verify the resulting project/version on the target index and install that published version in a fresh environment. Report the target, artifact names, and verification outcome without exposing credentials.
