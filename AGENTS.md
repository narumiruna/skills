# Repository Guidelines

Follow global defaults; this file contains only repository-specific additions and overrides.

## Communication & Documentation

- Lead with the main point and explain it simply before adding necessary detail.
- Use a clear structure, familiar words, and short, accurate sentences; omit repetition and unnecessary detail.
- Make documented rules specific and verifiable.
- Follow the model-selection policy in `./writing/skills/prompt-gpt/SKILL.md` when creating, revising, or reviewing skills and other agent-facing prompts.
- Use `README.md` for how the project is presented to users and how they install and discover skills; document maintainer workflow here.
  - Update the README catalog when a skill is added, deprecated, renamed, or recategorized, or when its trigger changes materially.
  - Keep a skill's frontmatter description and catalog entry aligned when its trigger or purpose changes.
- Update installation documentation and executable recipes only in the files that own the affected flow.

## Code Style

- Follow KISS (Keep It Simple) and YAGNI (You Aren't Gonna Need It).
- Use lowercase kebab-case for skill directories and name every required entry file exactly `SKILL.md`.
- Preserve a skill's original intent when naming or renaming it; use `<verb-ing>-<object>` only if it preserves that intent.
- Keep skills that serve as useful explicit mode shortcuts, even if their behavior can be inferred; keep `explain-step-by-step` active.
- Keep examples repository-relative and executable when practical.
- Use uv with PEP 723 inline metadata for new or modified standalone Python scripts, following the [official script guide](https://docs.astral.sh/uv/guides/scripts/).
  - Initialize new scripts with `uv init --script path/to/script.py` and declare dependencies in the `# /// script` block, using `dependencies = []` when none are required.
  - Add or update third-party dependencies with `uv add --script path/to/script.py <package>`.
  - Run scripts with `uv run path/to/script.py`.
  - For direct execution, use `#!/usr/bin/env -S uv run --script` as the first line and set the executable bit; the shebang does not replace dependency metadata.
- Apply Apple-derived design principles to user interfaces while adapting metrics and controls to the target platform.
  - Reduce cognitive load without removing needed features.
  - Keep critical actions and state visible, and reveal secondary controls and details in predictable steps.

## Boundaries

- For answers, explanations, reviews, diagnoses, and plans, inspect the relevant materials and report without editing.
- For changes, builds, and fixes, make the requested local changes and run relevant safe checks without asking first.
- Ask before writing to external systems, taking destructive or costly actions, or materially expanding the scope.
  - Ask before running `scripts/download_human_interface_guidelines.py`; by default, it downloads a large external corpus.
    - When maintaining the archiver, enumerate the DocC navigator and page JSON under `/tutorials/data/` instead of recursively downloading HTML.
- Do not hand-edit or commit ignored `build/` content; it is generated.
- Do not introduce root-level marketplace or plugin metadata unless corresponding repository files and workflows exist.

## Testing

- This repository has no maintained automated test suite; do not add or maintain repository tests or use test-driven development.
- Exercise each changed bundled script through a non-destructive path that covers the changed behavior.
  - Report the command and result, and name any paths you could not verify because of credentials, network access, or missing dependencies.
- If one-off `uv run --with ...` validation fails because `~/.cache/uv` is read-only, set `UV_CACHE_DIR=/tmp/uv-cache`.
  - Request temporary network access only if an uncached dependency still cannot resolve.
- Run `prek run -a` for repository-wide formatting and lint checks, and report any failure before opening a pull request.
- Run `prek run lint-python-scripts -a` to check PEP 723 metadata, dependency and Python version specifiers, and executable headers for all tracked `.py` files, including helpers and files under `deprecated/`.
  - The linter does not infer dependencies from imports.
- Run `git diff --check` and review the final diff for out-of-scope changes or repeated guidance.
- For changes under `examples/slides/`, verify the source assets.

## Repository structure

- Keep active skills in their source roots:
  - Global skills: `skills/<skill-name>/SKILL.md`, except for grouped skills at `skills/design/<skill-name>/SKILL.md` and `skills/sim/<skill-name>/SKILL.md`.
  - Category skills: `{writing,research,visuals,design,code-quality,workflow}/skills/<skill-name>/SKILL.md`, with no deeper category directories.
- `.agents/skills` is a tracked symlink to `skills/` for local discovery, not a separate source root.
- Keep deprecated skills in `deprecated/<skill-name>/SKILL.md`, outside active discovery.
- Keep optional supporting material inside its skill directory under `references/`, `scripts/`, `assets/`, or `agents/`.
- Keep source slides and visual examples under `examples/`.

## Git and commits

- In pull requests, summarize what changed and why, list affected paths, and report verification results, including skipped or failed checks.
- For changes under `examples/slides/`, include the generated preview or screenshots in the pull request; for slide visual changes elsewhere, include screenshots or links to rendered output.
