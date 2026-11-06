---
name: apply-google-typescript-style
description: Write, refactor, or review TypeScript code using Google's TypeScript Style Guide, focusing on module boundaries, type choices, class and callback rules, and Google-specific restrictions rather than basic TypeScript syntax.
---

# Apply Google TypeScript Style

Use these selected rules from the [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) as an addition to standard TypeScript practice, not a complete copy of the guide.

## Establish Scope

- Inspect repository instructions, `tsconfig` files, framework contracts, build scripts, and formatter and lint configuration before applying the rules.
- Respect explicit repository policies and required framework contracts.
  - If they conflict with a Google rule, preserve the required behavior and report the deviation.
  - Do not silently change compiler options, replace tooling, or break a framework-required default export to enforce this skill.
- Keep review-only requests read-only, and keep changes within the requested scope.
  Do not turn a bounded change into a repository-wide style migration.
- Preserve the guide's distinction between requirements and recommendations: `prefer` and `avoid` are not absolute prohibitions.
  Do not enforce incidental formatting choices from examples as rules.
- Consult the linked source section when an exception or omitted rule affects the task; do not require a full guide download for routine work.

## Modules and Export Boundaries

Sources: [imports](https://google.github.io/styleguide/tsguide.html#imports), [exports](https://google.github.io/styleguide/tsguide.html#exports), and [type-only imports and exports](https://google.github.io/styleguide/tsguide.html#import-and-export-type).

- Use ES module imports and exports, not `require` or TypeScript namespaces.
  - Namespaces are allowed only when required to interface with external code.
- Use named exports, not default exports.
  - Default imports are allowed for external code that requires them.
- Export only symbols used outside the module.
  Do not use `export let` or other exports whose binding changes after module initialization; expose changing values through getter functions instead.
- Export individual functions and constants rather than container classes used only for namespacing.
- Prefer relative imports within the same logical project, while avoiding excessive parent-directory steps.
- Prefer named imports for frequently used or clearly named symbols, and namespace imports for many symbols from a large API or names that need context.
- `import type` is allowed for type-only references; use `export type` when re-exporting a type.
  Use regular imports for runtime values and explicit side-effect imports for required initialization.
  Do not use `import('...')` inside type annotations.

## Type Choices and Assertions

Sources: [type system](https://google.github.io/styleguide/tsguide.html#type-system) and [type and non-nullability assertions](https://google.github.io/styleguide/tsguide.html#type-and-non-nullability-assertions).

- Use interfaces for object shapes rather than object-literal type aliases or classes with no implementation.
  Type aliases remain useful for unions, primitives, tuples, and other type expressions.
- Leave out annotations for trivially inferred local literals and redundant generic arguments.
  Do not require every function to have a return type annotation; honor local policy and export annotations needed by `isolatedDeclarations`.
- Add `|null` or `|undefined` where a type alias is used, not inside the alias itself.
  Neither absence value is preferred in all contexts.
- Use `T[]` and `readonly T[]` for simple or qualified element types, and `T[][]` for simple non-readonly multidimensional arrays.
  Use `Array<T>` or `ReadonlyArray<T>` at complex levels, such as `Array<string|number>` or `ReadonlyArray<string[]>`.
- Prefer a specific type or `unknown` with narrowing over `any`.
  - When `any` is legitimate, such as a deliberately partial test mock, use a narrow lint suppression and explain why it is needed.
- Avoid `{}` for opaque values or dictionaries; choose `unknown`, `object`, or `Record<string, T>` according to the required contract.
- Use the simplest type construct that expresses the contract.
  Mapped and conditional types are allowed, but do not replace a clear interface with a harder-to-read type expression just to remove repetition.
- Avoid APIs whose generic parameter appears only in the return type.
  - When using an existing API with this pattern, provide the generic argument explicitly.
- Prefer runtime checks and narrowing over type or non-null assertions.
  - Use assertions only when safety is obvious or explained in a comment.
  - Use `as` syntax, and pass through `unknown`, not `any` or `{}`, when a justified double assertion is needed.
- Annotate object literals with their intended type instead of asserting them with `as`; annotations preserve checks for misspelled or missing fields.

## Classes and Callbacks

Sources: [classes](https://google.github.io/styleguide/tsguide.html#classes) and [functions](https://google.github.io/styleguide/tsguide.html#functions).

- Use TypeScript `private`, not JavaScript `#private` fields.
  Omit the `public` modifier except on non-readonly public constructor parameter properties.
- Mark properties `readonly` when they are not reassigned after construction; this does not imply deep immutability.
- Use parameter properties for simple constructor assignments.
  Initialize independent fields at their declaration, and avoid reading constructor parameter properties from field initializers.
- Keep getters pure, with consistent results and no observable side effects.
  At least one accessor for a property must be non-trivial; do not add pass-through accessor pairs only to hide a field.
- Prefer function declarations for named functions and arrow functions for callbacks.
  - Function expressions are allowed only for generators or necessary dynamic rebinding of `this`.
- Prefer callback wrappers that explicitly forward arguments, rather than passing named functions whose optional parameters might be supplied by the caller.
  Do not pass unbound instance methods; use an arrow wrapper to preserve `this`.
- Prefer class methods over arrow-function fields.
  - Arrow-function fields are appropriate when a removable event handler needs a stable bound reference, and may be clearer for template bindings.
  - Do not call `bind` in the expression that installs an event handler; the temporary reference prevents later removal.
- Do not use `this` in a static context.
  Prefer module-local functions over private static helpers when readability is not reduced.

## Errors and Control Flow

Sources: [control structures](https://google.github.io/styleguide/tsguide.html#control-structures) and [type coercion](https://google.github.io/styleguide/tsguide.html#type-coercion).

- Create errors with `new Error()` or an `Error` subclass, and throw only `Error` instances.
  - Explicit rejection reasons, abort reasons, and `ErrorOptions.cause` must also be `Error` instances.
  - Calling an abort API without a reason is allowed; it supplies an abort error.
- Do not add speculative handling of non-`Error` values to an Error-only API contract.
  - If a called API is known to throw other values, document that source and handle those values as needed.
- Keep `try` blocks focused where readability permits, and explain intentionally ignored exceptions in a comment.
- Use `Number` for string-to-number conversion, not unary `+` or `parseFloat`, and handle non-throwing failures such as `NaN`.
  - Use `parseInt` only when a non-decimal radix is required; validate the whole input before parsing and check the result for `NaN`.
- Compare enum values explicitly instead of converting them to booleans, including implicit truthiness checks.
- Give every `switch` a final `default` group, and do not let non-empty case groups fall through.
- Use `===` and `!==`.
  - Comparisons with literal `null` may use `==` or `!=` to cover both `null` and `undefined`.

## Google-Specific Feature Limits

Sources: [disallowed features](https://google.github.io/styleguide/tsguide.html#disallowed-features), [decorators](https://google.github.io/styleguide/tsguide.html#decorators), and [compiler error suppression](https://google.github.io/styleguide/tsguide.html#ts-ignore).

- Use ordinary `enum`, not `const enum`; do not treat all enums as forbidden.
- Do not define new decorators.
  The guide permits existing Angular and Polymer decorators, not arbitrary decorator libraries.
- Do not use `@ts-ignore`, `@ts-nocheck`, or production `@ts-expect-error`.
  - `@ts-expect-error` is permitted but discouraged in unit tests; prefer a focused, documented cast or lint suppression when suitable.

## Names and Documentation

Sources: [naming](https://google.github.io/styleguide/tsguide.html#naming) and [comments and documentation](https://google.github.io/styleguide/tsguide.html#comments-and-documentation).

- Use `UpperCamelCase` for types, classes, enums, and component functions in TSX; use `lowerCamelCase` for ordinary functions, variables, methods, and properties.
- Use `CONSTANT_CASE` for values intended to remain unchanged at module scope, in module-level enums, or as static fields of module-level classes.
  - Arrow functions that implement an interface may use `lowerCamelCase`.
  - Local bindings normally use `lowerCamelCase`; aliases keep the original symbol's casing.
- Treat acronyms as words, such as `loadHttpUrl`, not `loadHTTPURL`.
  Do not add `I` prefixes or `Interface` suffixes unless they are idiomatic in the target environment.
- Do not mark private members with leading or trailing underscores.
  Use `_name` only for syntactically required unused identifiers; omit trailing unused callback parameters.
- Document top-level exports and non-obvious members with useful JSDoc, not restatements of their names.
  - Tooling-only exports do not require comments.
  - Do not repeat TypeScript types or modifiers in JSDoc tags, and put documentation before decorators.
- Include clear call-site migration directions in `@deprecated` comments.

## Verify

Use the target repository's existing formatter, type checker, lints, and relevant tests.
For reviews, cite the source rule, check its exceptions, and distinguish project-policy conflicts from defects.
For changes, report affected paths, checks run, and any unverified behavior; do not claim full guide compliance from this selected subset.
