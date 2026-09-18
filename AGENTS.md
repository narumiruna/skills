# Repository Guidelines

Follow global defaults; this file contains only repository-specific additions and overrides.

## Communication & Documentation

- Lead with the most important relevant information and omit anything unnecessary or repeated.
- Use clear structure, familiar words, and concise sentences.
- Explain the main idea simply before adding necessary detail.
- Keep information accurate.
- Make documented rules specific and verifiable.
- Follow the model-selection policy in `./skills/default/prompt-gpt/SKILL.md` when creating, revising, or reviewing skills and other agent-facing prompts.
- Keep external positioning, installation flows, and skill discovery in `README.md`, and keep maintainer workflow in this file.
- Update the README catalog when a skill is added, deprecated, renamed, recategorized, or materially changes its trigger.
- Update installation documentation and executable recipes only in the files that own the affected flow.

## Code Style

- Follow KISS (Keep It Simple) and YAGNI (You Aren't Gonna Need It).
- Prefer simple, minimal solutions over unnecessary complexity.
- Use lowercase kebab-case for skill directories and name every required entry file exactly `SKILL.md`.
- Preserve a skill's original user intent when naming or renaming it; do not force `<verb-ing>-<object>` when that changes the meaning.
- Retain explicit-invocation skills that provide useful mode shortcuts even when their behavior can be inferred; keep `explain-step-by-step` active.
- Keep a skill's frontmatter description and README catalog entry aligned when its trigger or purpose changes.
- Keep examples repository-relative and executable when practical.
- For user interfaces, apply Apple-derived design philosophy across platforms while translating platform-specific metrics and controls to target conventions; minimize cognitive load without sacrificing functional completeness, keep critical actions and state visible, and use predictable progressive disclosure for secondary complexity.

## Boundaries

- For answer, explanation, review, diagnosis, or planning requests, inspect the relevant materials and report without making changes.
- For change, build, or fix requests, make the requested in-scope local changes and run relevant safe checks without asking first.
- Ask before writing to external systems, taking destructive or costly actions, or materially expanding the scope.
- Ask before running `scripts/download_human_interface_guidelines.py` because its default mode downloads a large external corpus; when maintaining the archiver, enumerate the DocC navigator and page JSON under `/tutorials/data/` instead of recursively downloading HTML.
- Treat ignored `build/` content as generated output; do not hand-edit or commit it.
- Treat `skills/default/` and `skills/optional/` as the active source roots; `.agents/skills` is a tracked local-discovery symlink to `skills/default/`, not a second copy to edit.
- Do not introduce root-level marketplace or plugin metadata unless corresponding repository files and workflows exist.

## Testing

- This repository has no maintained automated test suite; do not add or maintain repository tests or apply TDD to repository changes.
- Run every changed bundled script through a non-destructive path that exercises the changed behavior; report the command and result, and identify any path that credentials, network access, or unavailable dependencies prevented you from verifying.
- If one-off `uv run --with ...` validation fails because `~/.cache/uv` is read-only, set `UV_CACHE_DIR=/tmp/uv-cache`; request temporary network access only when an uncached dependency still cannot resolve.
- Run `prek run -a` as the repository-wide formatting and lint gate, and report any failure before a pull request.
- Run `git diff --check` and inspect the final diff for unintended scope or repeated guidance.
- For changes under `examples/slides/`, verify source assets and include the generated preview or screenshots in the pull request.

## Repository structure

- Keep default skills directly in `skills/default/<skill-name>/SKILL.md` and optional skills directly in `skills/optional/<skill-name>/SKILL.md`; do not add deeper category directories.
- Keep deprecated skills in `deprecated/<skill-name>/SKILL.md`, outside active discovery.
- Keep optional supporting material inside its skill directory under `references/`, `scripts/`, `assets/`, or `agents/`.
- Keep source slides and visual examples under `examples/`.

## Git and commits

- In pull requests, summarize what changed and why, list affected paths, and report verification outcomes with any skipped or failing check.
- Add screenshots or rendered output links for slide visual changes.
