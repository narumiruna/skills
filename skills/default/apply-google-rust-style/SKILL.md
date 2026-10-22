---
name: apply-google-rust-style
description: Write, refactor, or review Rust code using Google's Rust Style Guide, focusing on non-obvious import conventions, API design choices, panic restrictions, and API evolution rather than basic Rust rules.
---

# Apply Google Rust Style

Use these selected rules from the [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html) as an addition to standard Rust practice, not a complete copy of the guide.

## Establish Scope

- Inspect repository instructions, build system, toolchain, and formatter configuration before applying the rules.
- Distinguish reusable library APIs from application code.
  API design rules are binding for libraries that adopt this guide, but are strong recommendations for applications, where direct solutions can be better.
- Keep review-only requests read-only.
  Do not turn a bounded change into a repository-wide style migration.
- Load [codebase-specific rules](references/codebases.md) only for Chromium, Android, or Fuchsia work.
  Do not apply their restrictions to ordinary Cargo projects.
- Consult the linked source section when an exception or omitted rule affects the task; do not require a full guide download for routine work.

## Imports and Module Boundaries

Source: [code organization](https://google.github.io/styleguide/rustguide.html#code-organization).

- Keep non-leaf modules limited to module declarations and re-exports, apart from a small amount of connecting implementation code.
  Inline test modules and cross-language binding modules do not prevent a module from counting as a leaf.
- Import items from one module per `use` statement: `use foo::bar::{Bar, Baz};`, not `use foo::{Foo, bar::Bar};`.
  This corresponds to `imports_granularity = Module`; do not require nightly Rust solely to configure it.
- Prefer function-local trait imports unless their methods are used extensively throughout the file.
- Qualify free functions from other modules with the module name, but import types and traits for unqualified use.
  - Direct function imports are allowed for sufficiently distinct names or when the module name itself would collide.
  - Qualified or renamed types are allowed for ambiguous names, large type groups, generated code, macros, or import blocks that would otherwise become excessive.
- Avoid defining preludes and using glob imports.
  - Allowed cases are `super::*` in inline modules, enum variants inside functions primarily handling that enum, and submodule re-exports in non-leaf modules.
  - Third-party preludes need reviewer judgment.
  - C++ namespace merging may use globs only inside a private merged module.

## API Choices That Differ by Context

Sources: [inputs and outputs](https://google.github.io/styleguide/rustguide.html#inputs-and-outputs), [traits](https://google.github.io/styleguide/rustguide.html#traits), and [initialization names](https://google.github.io/styleguide/rustguide.html#naming-initialization-functions).

- Application code should almost never accept `impl Into<T>` parameters.
  In libraries, consider them only when call-site convenience outweighs generic complexity and code size.
- For reusable libraries that only iterate over input, prefer iterator or `IntoIterator` parameters; prefer iterator return types over forced collection allocation.
  - Application code may use slices and `Vec` when they simplify the code without a clear flexibility or performance loss.
  - Returning a `Vec` is also appropriate when callers need ownership or indexing, the implementation naturally creates or already owns one, or a clearer loop makes allocation acceptable.
- Name constructors `new()` or `new_with_foo()`; use `try_new()` when the constructor returns `Result`.
  Pair an important `From` implementation with an explicit inherent constructor or conversion method for discoverability.
- For operator support alone, prefer `PartialEq` over `Eq` and `PartialOrd` over `Ord`.
  Add the stronger traits when their stronger contracts are valid and needed, such as `Eq` with `Hash` for map keys.
- Implement `Copy` for error types whenever possible.
  Add trait implementations as needed in application code; low-level libraries should anticipate likely user needs.
- Keep extension traits with the team that owns the original type, except for widely useful foundational or framework extensions.
  Use the `Ext` suffix, and do not introduce traits merely to organize methods.

## Failure and Safety Restrictions

Sources: [poisoned mutexes](https://google.github.io/styleguide/rustguide.html#poison), [panic recovery](https://google.github.io/styleguide/rustguide.html#catch-unwind), [global initialization](https://google.github.io/styleguide/rustguide.html#global-initialization), and [unsafe code](https://google.github.io/styleguide/rustguide.html#unsafe).

- Do not recover access to the contents of a poisoned mutex.
- Do not use `panic::catch_unwind` in first-party code as a correctness mechanism.
  The only exception is defense in depth in code that already works to avoid panics and can run with `panic=unwind`; no required property may depend on recovery.
- Do not arrange for code to run before `main()`, for example with the `ctor` crate.
- In addition to safety comments, justify why unsafe code cannot use an equivalent safe implementation.
  If the reason is performance, supply benchmark evidence.
  The justification may cover a block, file, or build target.

## API Evolution and Matching

Source: [other Rust features](https://google.github.io/styleguide/rustguide.html#other-features) and [non-exhaustive matching](https://google.github.io/styleguide/rustguide.html#non-exhaustive-enum-matching).

- Use `#[non_exhaustive]` for public enums and structs with public fields used across team boundaries.
  - Exceptions include stable variants or fields, a commitment to migrate all affected callers, or a small usage scope.
  - Structs may also omit it to support external struct update syntax such as `Options { field, ..Default::default() }`.
- When matching a non-exhaustive enum, explicitly list known variants, including ignored variants grouped with the wildcard arm.
  If only selected variants matter, prefer `if let` or `let ... else`, unless `match` is clearer.
- Treat another owner's `#[doc(hidden)]` items as private.
- Make a public function `const` only if it can remain `const`, or if there is a commitment to help callers migrate.

## Verify

Use the target repository's formatter, lints, and relevant tests.
For reviews, cite the violated rule and check its exceptions before reporting a finding.
For changes, report the affected paths, checks run, and any unverified behavior; do not claim full guide compliance from this selected subset.
