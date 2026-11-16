# AGENTS.md Templates

## Default Sections

Use these sections as a checklist when creating or restructuring an `AGENTS.md` file.
Check every unmarked section and preserve this relative order among the sections that remain.
Include a section only when it has verified guidance that an agent needs.
Omit it after inspection when no such guidance exists instead of leaving it empty or inventing rules.
Consider sections marked `[Optional]` only when they are relevant to the repository.
The `[Optional]` marker is a template annotation; remove it from headings included in the final file.

```markdown
## [Optional] Communication
## Documentation
## Code style
## Commands
## Boundaries
## [Optional] Security
## Testing
## [Optional] Project overview
## [Optional] Repository structure
## [Optional] Git and commits
```

## Action Policy

When action policy is needed, keep one compact block:

```text
For answer, explanation, review, diagnosis, or planning requests, inspect the relevant materials and report the result.
Do not make changes unless the request asks for them.
For change, build, or fix requests, make the requested local changes and run relevant safe checks.
Ask before writing to external systems, taking destructive or costly actions, or greatly expanding the scope.
```

Adapt the policy to evidence from the repository.
Name safe local actions and project-specific exceptions.
Do not repeat the policy elsewhere.
