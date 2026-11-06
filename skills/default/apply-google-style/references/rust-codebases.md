# Codebase-Specific Rust Rules

Use these rules only in the named codebase, after checking its current local instructions.
Source: [Google Rust Style Guide](https://google.github.io/styleguide/rustguide.html).

## Chromium

- Prefer small crates focused on one abstraction, ideally a single file.
  Larger crates are allowed for trait coherence requirements or large foundational libraries.
- Keep all `.rs` files for one `rust_library` in a single directory without subdirectories.
  The exception is Cargo-built Rust code in `//third_party`, which uses conventional Cargo layout.
- Use `chromium::import!()` for imports and the repository's formatter, such as `git cl format`.
- Direct imports of free functions from small, single-purpose first-party crates are allowed.
- Do not use `async` or `.await`.
- Prefer sequences rather than starting threads through the Rust standard library.
- Use `rust_gtest_interop` for tests rather than assuming `#[test]` integrates with the build.
- Unstable features need codebase-wide approval by the style arbiters; typically they must have a clear path to stabilization.

## Fuchsia

- Use `fuchsia_sync::Mutex`, not `std::sync::Mutex` or `parking_lot::Mutex`.
- Use `#[fuchsia::test]` for tests.
- Check [Fuchsia's unstable-feature policy](https://fuchsia.dev/fuchsia-src/development/languages/rust/unstable) before using unstable features.

## Android

Embedded programming may use unstable features required to build an artifact correctly, but review is still required to look for alternatives.

## Panic Mode

Chromium, Android, and Fuchsia require `panic=abort` according to the guide.
The defense-in-depth exception for `catch_unwind` therefore does not apply to these codebases.
