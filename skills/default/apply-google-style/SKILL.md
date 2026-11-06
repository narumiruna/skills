---
name: apply-google-style
description: Write, refactor, or review code and documentation using the guides in Google's style guide index for Angular, C++, C#, Common Lisp, Dart, Go, Haskell, HTML/CSS, Java, JavaScript, JSON, Kotlin, Markdown, Objective-C/Objective-C++, Python, R, Rust, Shell/Bash, Swift, Tcl/Tk, TypeScript, Verilog/SystemVerilog, Vim script, and XML.
---

# Apply Google Style

Use the guide for each language or format in the requested work.
The catalog below covers all 24 guides in the [Google Style Guides index](https://google.github.io/styleguide/), including guides hosted by other projects.

## Establish Scope

- Inspect repository instructions, framework contracts, build scripts, toolchain, and formatter and lint configuration, including language-specific settings such as `tsconfig` files.
- Keep review-only requests read-only, and keep changes within the requested scope.
  Do not turn a bounded change into a repository-wide style migration.
- Respect explicit repository policies and required framework contracts.
  - If they conflict with a guide rule, preserve required behavior and report the deviation.
  - Do not silently change compiler options, replace tooling, or break framework-required exports merely to enforce style.
- Keep requirements, recommendations, and exceptions distinct.
  Do not treat `prefer` or `avoid` as absolute prohibitions, or enforce incidental formatting from examples as rules.

## Select and Read the Guides

- Select only the guides for the affected languages and formats.
  Read the relevant source sections, not the full collection.
- For Rust and TypeScript, load the linked local selected rules first.
  Consult the upstream guide when an omitted rule, an exception, or a possible source change affects the task.
- For other languages and formats, read the applicable sections of the linked guide before applying or reporting its rules.
- Apply each rule only within its guide's stated language and context.
  Do not transfer restrictions between languages or treat framework and codebase policies as universal Google rules.
- For Angular work, combine the framework guide with the TypeScript and HTML/CSS guides as applicable.
  Do not substitute JavaScript rules for conflicting TypeScript rules.
- Use the upstream index to resolve moved guides or find newly added entries.
  If a source cannot be read, identify the gap and continue only with available project rules or local selected rules; do not invent source requirements.

| Language or format | Sources, scope, and local references |
| --- | --- |
| Angular | [Angular Style Guide](https://angular.dev/style-guide) |
| C++ | [C++ Style Guide](https://google.github.io/styleguide/cppguide.html) |
| C# | [C# Style Guide](https://google.github.io/styleguide/csharpguide.html) |
| Common Lisp | [Common Lisp Style Guide](https://google.github.io/styleguide/lispguide.html) |
| Dart | [Effective Dart](https://dart.dev/effective-dart): [style](https://dart.dev/effective-dart/style), [documentation](https://dart.dev/effective-dart/documentation), [usage](https://dart.dev/effective-dart/usage), and [design](https://dart.dev/effective-dart/design). |
| Go | [Overview](https://google.github.io/styleguide/go/); the [core guide](https://google.github.io/styleguide/go/guide) takes precedence over [decisions](https://google.github.io/styleguide/go/decisions); [best practices](https://google.github.io/styleguide/go/best-practices) are recommendations. |
| Haskell | [Haskell Style Guide](https://google.github.io/styleguide/haskellguide.html) |
| HTML/CSS | [HTML/CSS Style Guide](https://google.github.io/styleguide/htmlcssguide.html) |
| Java | [Java Style Guide](https://google.github.io/styleguide/javaguide.html) |
| JavaScript | [JavaScript Style Guide](https://google.github.io/styleguide/jsguide.html), no longer updated. |
| JSON | [JSON Style Guide](https://google.github.io/styleguide/jsoncguide.html) for API requests and responses, not arbitrary configuration files or JSONC. |
| Kotlin | [Kotlin Style Guide](https://developer.android.com/kotlin/style-guide), Google's Android coding standards. |
| Markdown | [Markdown Style Guide](https://google.github.io/styleguide/docguide/style.html) |
| Objective-C/Objective-C++ | [Objective-C Style Guide](https://google.github.io/styleguide/objcguide.html) |
| Python | [Python Style Guide](https://google.github.io/styleguide/pyguide.html) |
| R | [R Style Guide](https://google.github.io/styleguide/Rguide.html), Google's differences from the [Tidyverse Style Guide](https://style.tidyverse.org/). |
| Rust | [Rust Style Guide](https://google.github.io/styleguide/rustguide.html); [selected rules](references/rust.md) |
| Shell/Bash | [Shell Style Guide](https://google.github.io/styleguide/shellguide.html) |
| Swift | [Swift Style Guide](https://google.github.io/swift/) |
| Tcl/Tk | [Dodekalogue](https://wiki.tcl-lang.org/page/Dodekalogue), a community Tcl syntax and semantics reference, not a Tk UI style policy. |
| TypeScript | [TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html); [selected rules](references/typescript.md) |
| Verilog/SystemVerilog | [Verilog Style Guide](https://google.github.io/styleguide/verilogguide.html), including synthesizable and testbench code. |
| Vim script | [Vim script Style Guide](https://google.github.io/styleguide/vimscriptguide.html) and [full guide](https://google.github.io/styleguide/vimscriptfull.html). |
| XML | [XML Document Format Style Guide](https://google.github.io/styleguide/xmlguide.html), primarily for new machine-oriented formats, not rich text or forced retroactive redesign. |

## Verify and Report

- Use the target repository's existing formatter, type checker, lints, and relevant tests for the requested scope.
- For reviews, cite the source rule and location, check its exceptions, and separate confirmed violations from recommendations and project-policy conflicts.
- For changes, report affected paths, checks run, deviations, and any unverified behavior or unavailable source.
- Do not claim full guide compliance from a selected rule summary or formatter output alone.
