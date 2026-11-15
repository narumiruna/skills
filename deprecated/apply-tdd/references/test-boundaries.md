# Test Boundaries

These are conservative policy fallbacks, not claims that every project in an ecosystem uses the same layout. Resolve the repository's established source and test roots first; more-specific repository instructions override this reference.

A work unit enters TDD only when:

1. its production path belongs to a repository-established source root or, when that cannot be established, the matching fallback below
2. it passes the behavior gate in `SKILL.md`
3. its test uses only repository-established or fallback test-owned inputs

For an unlisted ecosystem, use the general behavior gate and repository evidence rather than inventing a layout.

## Resolve Source and Test Layouts

1. Find the nearest package, module, or workspace boundary from the ecosystem manifest.
2. Inspect build/package configuration, exports, imports, source-control patterns, test scripts, and runner configuration for the paths actually used by the project.
3. Prefer consistent existing production and test paths over ecosystem convention. Do not force a `src/` layout onto a flat-layout project.
4. Use the table's fallback only for the part of the layout that remains unresolved.

## Boundary List

| Ecosystem | Project boundary | Production behavior eligible for TDD | Test placement and owned inputs |
| --- | --- | --- | --- |
| Python | Nearest ancestor containing `pyproject.toml`, `setup.cfg`, or `setup.py` | Runtime package/module roots declared by build configuration or established imports. Fallback: `src/` when present, otherwise top-level import packages; exclude tooling, generated, and vendored code | Paths discovered from test configuration and established tests. Fallback: `tests/`; inline builders, fixtures under the resolved test root, temporary paths, mocks, and fakes |
| Rust | Nearest ancestor whose `Cargo.toml` defines a package; evaluate each workspace member separately | Behavior and packaged runtime resources under Cargo-established source targets; fallback: `src/`; exclude generated and vendored code | Unit and documentation tests attached to source targets; integration tests and fixtures under `tests/`; temporary paths, mocks, and fakes |
| Go | Nearest ancestor containing `go.mod`; evaluate each workspace module separately | Non-test, non-generated `.go` files in packages selected by `go list ./...`; exclude `vendor/` and `testdata/` | Colocated `*_test.go`; the target package's `testdata/`, `t.TempDir()`, mocks, fakes, and local in-process test servers |
| TypeScript | Nearest ancestor containing `package.json`; evaluate each monorepo member separately | Runtime roots established by `tsconfig`, package exports, build configuration, or imports. Fallback: `src/` when present, otherwise package-owned runtime files; exclude declarations, tooling, generated code, tests, fixtures, and mocks | Files discovered by the configured runner; fallback: `tests/**/*.test.{ts,tsx,mts,cts}`; test-owned fixtures, temporary paths, mocks, and fakes |
| JavaScript | Nearest ancestor containing `package.json`; evaluate each monorepo member separately | Runtime roots established by package exports, build configuration, or imports. Fallback: `src/` when present, otherwise package-owned runtime files; exclude tooling, generated code, tests, fixtures, and mocks | Files discovered by the configured runner; fallback: `tests/**/*.test.{js,jsx,mjs,cjs}`; test-owned fixtures, temporary paths, mocks, and fakes |

## Isolation Rules

- Test only behavior provided by the eligible production path. Helpers and fixtures are support code, not the subject under test.
- Exercise a stable interface; do not inspect source text or repeat static source or config values in assertions.
- If eligible behavior normally reads data from outside its production path, recreate the smallest representative input in a permitted fixture location or per-test temporary workspace, then pass or inject it.
- Tests may import ordinary dependencies, but replace external side effects with controlled test doubles or local in-process substitutes.
- Test code must not open or assert against real manifests, lockfiles, tool configuration, scripts, migrations, examples, benchmarks, build output, user files, host environment values, network services, or databases. Build and test tools may still read their own configuration to compile and discover tests.
- A production change outside the resolved eligible roots is outside TDD. Tests may still be added in the resolved test location for eligible production behavior.

## Ecosystem-Specific Rules

### Python

For a `src/` layout, test `src/package/config.py` with data under the resolved test fixture root or generated in a temporary directory. For a flat layout, use the package root established by build configuration or imports. Do not read the project's real `pyproject.toml` as test data.

### Rust

Keep focused unit tests in `#[cfg(test)]` modules beside the behavior. Use `tests/` for public integration behavior and documentation tests for documented public examples. Treat `build.rs`, `examples/`, `benches/`, manifests, lockfiles, and `target/` as outside TDD.

### Go

Use the package name when private access is necessary and its `_test` variant when testing only the exported contract. Keep static samples in that package's `testdata/`; the Go tool excludes this directory from normal package discovery. Use `t.TempDir()` for mutable files and `httptest` for HTTP behavior.

### TypeScript and JavaScript

Determine the runner from package scripts and runner configuration before choosing the test filename. Configuration controls discovery, but it is not test data.

- If the runner defines `include`, `testMatch`, or an equivalent matcher, the test must match it.
- Without a custom matcher, Vitest discovers `*.test.*` and `*.spec.*`; Jest discovers those suffixes and supported files under `__tests__/`.
- For another or unknown runner, use the conservative `tests/<behavior>.test.<extension>` fallback and invoke that file explicitly when supported.
- Store static data under a fixture or mock directory owned by the discovered test location; otherwise generate it in a per-test temporary directory.
- TypeScript declaration-only changes such as `.d.ts` are outside TDD; validate them with the configured type checker or type-test tooling.
- Treat package manifests, lockfiles, `tsconfig`, runner and bundler configuration, scripts, distribution output, coverage output, and real browser profiles as outside TDD.

## Outside-TDD Validation

Always run relevant existing tests or a focused smoke check plus the repository gate when available. Add the cheapest ecosystem-specific checks that cover the change:

| Ecosystem | Typical checks |
| --- | --- |
| Python | Parser or schema validation, lint, formatting, type checking, packaging, or build checks |
| Rust | `cargo fmt --check`, `cargo check`, Clippy, or package and workspace builds |
| Go | `gofmt`, `go vet`, package and module builds, migration checks, or generation checks |
| TypeScript | Configuration parsing, lint, formatting, type checking, or package builds |
| JavaScript | Configuration parsing, lint, formatting, package or bundle builds |

## Convention Basis

Source layouts are repository facts, not universal ecosystem rules. Python may use `src/` or a flat package layout; JavaScript and TypeScript have no single mandatory source root. Rust and Go expose stronger toolchain conventions, but workspace and target boundaries still require inspection. Test discovery must be verified against the active runner.

- [Python `src` layout versus flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Cargo package layout](https://doc.rust-lang.org/cargo/guide/project-layout.html)
- [Cargo tests](https://doc.rust-lang.org/cargo/guide/tests.html)
- [Go test packages](https://pkg.go.dev/cmd/go#hdr-Test_packages)
- [Vitest test inclusion](https://vitest.dev/config/include)
- [Jest `testMatch`](https://jestjs.io/docs/configuration#testmatch-arraystring)
- [Node.js test runner](https://nodejs.org/api/test.html#running-tests-from-the-command-line)

Add another ecosystem only when its production scope, test discovery, permitted inputs, and outside-boundary validation can all be defined explicitly.
