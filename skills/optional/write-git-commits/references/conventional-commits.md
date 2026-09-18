# Conventional Commits Reference

## Format

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

Use a lowercase type. Add a short noun-like scope only when it clarifies the affected area. Put `!` immediately before `:` for a breaking title. Separate title, body, and footers with blank lines.

## Common Types

- `feat`: new capability
- `fix`: incorrect behavior or regression
- `docs`: documentation only
- `refactor`: structure with no intended behavior change
- `perf`: performance improvement
- `test`: tests only
- `build`: build or packaging
- `ci`: CI automation
- `style`: formatting only
- `chore`: maintenance not better described above
- `revert`: an earlier change is reverted

Split a change when unrelated intents honestly require different types.

## Body, Footers, and Breaking Changes

Use the body for why, constraints, edge cases, or tradeoffs the title cannot carry. Use footers only for real repository-supported trailers, such as `Refs: #123`.

Mark breaking behavior with `!`, a `BREAKING CHANGE:` footer, or both. Use the footer when impact or migration guidance needs explanation:

```text
feat(api)!: remove v1 session endpoint

BREAKING CHANGE: clients must migrate to the v2 session endpoint.
```

Repository instructions own attribution and other local trailer policies.
