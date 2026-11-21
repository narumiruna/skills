# Skills

Reusable agent skills for coding, writing, research, and slide work. This repo is organized for Codex-first workflows and can also be installed as a standard skills repo.

## 🚀 Quick Start

The `./skills/` directory is my global skill collection. `just install` links
it to `~/.agents/skills/`. To install the collection globally without a local
checkout, run:

```shell
npx skills add narumiruna/skills/skills --global
```

Add [project skills](#project-skills) as needed for each project.

Then open Codex and run `/skills` to inspect what was installed. Invoke a skill explicitly with `$skill-name`, or describe the task normally and let Codex choose a match.

## 📦 Install

### Standard install with `npx skills`

When using `npx skills`, install the global groups under `skills/design/` and
`skills/sim/` separately as needed. `just install` includes both groups.

```shell
npx skills add narumiruna/skills/skills/design --global
npx skills add narumiruna/skills/skills/sim --global
```

#### Project skills

The other active skills are grouped by category for installation into individual
projects. From your project directory, run
`npx skills add narumiruna/skills/<category>`, replacing `<category>` with a
top-level directory name such as `writing`. Omit `--global` to install into the
current project.

```shell
npx skills add narumiruna/skills/writing
npx skills add narumiruna/skills/research
npx skills add narumiruna/skills/visuals
npx skills add narumiruna/skills/design
npx skills add narumiruna/skills/code-quality
npx skills add narumiruna/skills/workflow
```

The former `optional/skills/` collection is now split across the six category roots below; replace its old install command with the categories you need.

### Local checkout with a directory symlink

Use this when you want `~/.agents/skills` to track a local checkout. Install
[just](https://just.systems/) and Bash. The installer uses Bash for path checks
and supports macOS BSD `ln` and GNU `ln`; no additional Coreutils installation
is required. Then run:

```shell
just install
```

This creates one symlink, `~/.agents/skills`, pointing to this checkout's entire
`skills/` directory. GNU Stow is not required. Category collections are not
included. Running `just install` again leaves the same link unchanged. The
recipes call [`scripts/manage-skills.sh`](scripts/manage-skills.sh) to manage
the symlink.

Installation refuses to replace a directory that contains this checkout or its
source `skills/` directory, including when the target equals either directory.
It also refuses to replace directories inside the source `skills/` directory.
These checks resolve symlinks, ignore `CDPATH`, and run before the menu, backup,
or deletion.

For other existing real directories, `just install` asks how to handle them,
including directories created by the previous Stow-based recipe:

1. Back up: move the entire directory into a uniquely named
   `~/.agents/skills.backup.XXXXXX/` directory, then create the symlink. The backup
   contains the original `skills/` directory, and its location is printed.
2. Delete: permanently remove the directory and all its contents, then create
   the symlink.
3. Cancel: stop without changing the directory.

Pressing Enter, invalid input, or end-of-input also cancels. Cancellation exits
with a nonzero status.

`just reinstall` uses the same installation flow, so it also handles an existing
directory. Existing files and unrelated symlinks are not replaced; move those
aside before installing.

Remove only this checkout's directory symlink, without changing its contents:

```shell
just uninstall
```

`just uninstall` refuses to remove directories or unrelated symlinks. Before
moving the checkout, run `just uninstall`, then run `just install` from its new
location.

## 🧭 How To Use In Codex

- Run `/skills` to inspect the installed collection.
- Type `$review-code`, `$apply-imrad`, or another skill name to invoke one explicitly.
- Describe the task normally and let Codex choose a matching skill.

If Codex does not pick up a local skill change, restart Codex and try again.

## How To Use In Pi

Run Pi from this checkout or use `just install` for global discovery.
Run `/reload` in an open session after adding or renaming a skill.
Use `/skill:<name>` to invoke a skill with arguments:

```text
/skill:propose-ranked-options skills/address-pr-feedback/ naming
```

## 🧰 Skill Catalog

### Global Skills

Global skills live under `skills/` and are linked by `just install`.
`curate-ui-styles` and the [saved UI styles](#saved-ui-styles) are grouped under `skills/design/`.
The two Self-Improvement Memory (SIM) skills are grouped under `skills/sim/`.

| Skill | Use it for |
| --- | --- |
| `address-pr-feedback` | Handling PR comments, publishing in-scope fixes, and processing new feedback in a bounded bot review loop without waiting for human reviewers. Supports follow-up PRs after merge. |
| `apply-google-style` | Writing, refactoring, and reviewing code and documentation with all guides in Google's style guide index. |
| `collect-evolve-cases` | Explicitly previewing and importing reviewed evolve cases from local Pi sessions for one project. |
| `configure-ghostty` | Configuring, validating, diagnosing, and operating Ghostty with version-aware file, keybinding, runtime, and launch guidance. |
| `curate-ui-styles` | Create, compare, and fine-tune reusable UI style skills by comparing and answering A/B/C questions in one local browser tab. |
| `execute-plans` | Executing a plan on a focused branch and opening a PR by default after required local checks pass, with default-directory lookup when no full path is supplied; use `write-plans` to draft or track plan files. |
| `give-language-feedback` | Proactive, one-sentence grammar or wording feedback in any language alongside the main task, without requiring a language-help request. |
| `improve-agent-harnesses` | Testing and automatically applying measured improvements to skills under `~/.agents/skills/`, including itself, on request or after a reproducible skill failure. |
| `lean-verify` | Formalizing claims and constructing or checking Lean 4 proofs for mathematical theorems, program properties, algorithm correctness, and other formal-verification tasks in `~/.agents/lean`. |
| `propose-ranked-options` | Explicitly requesting improvement proposals for a target, such as naming, code refactoring, or UI/UX, ranked by a total score out of 100. |
| `prune-code-comments` | Auditing and pruning source comments, tracking workarounds as issues, moving decisions to ADRs, and preventing new comments with a lint baseline. |
| `resolve-github-issues` | Investigating GitHub issues, obtaining explicit plan approval, handing off to `write-plans` and `execute-plans`, then verifying and reporting the issue outcome. |
| `review-pull-requests` | Complete read-only PR assessments and merge verdicts, with pinned commits, base/head bug reproduction, impact, risks, and verification. |
| `write-agent-skills` | Creating and maintaining Agent Skills, including naming, reviewing, validating, and improving when they load and what they do. |
| `write-agents-md` | Creating, reviewing, and automatically maintaining lean, evidence-backed `AGENTS.md` guidance at the narrowest applicable scope. |
| `write-plans` | Drafting, revising, and tracking implementation plan files, completion evidence, external handoff, and completed-plan cleanup; use `execute-plans` for implementation-to-PR delivery. |

The former `create-agent-skills` skill is now named `write-agent-skills`.
The former `apply-google-rust-style` and `apply-google-typescript-style` skills are merged into `apply-google-style`.

### Category Skills

Category skills live under `<category>/skills/<skill-name>/` and remain available for selective installation.

#### Writing and Publishing

Source: `writing/skills/`.

| Skill | Use it for |
| --- | --- |
| `apply-asd-ste100` | Drafting, revising, and reviewing technical documentation with ASD-STE100 rule and vocabulary checks for the requested issue (Issue 9 by default), or clarity principles without a compliance claim. |
| `apply-imrad` | Evidence-traceable IMRaD fit checks, reviews, transformations, and drafts. |
| `calibrate-writing-style` | Explicit-invocation interviews that refine reusable English and Taiwan Traditional Chinese writing-style prompts. |
| `create-telegraph-pages` | Preparing and publishing one explicitly authorized Telegra.ph article. |
| `prompt-gpt` | Creating, revising, and reviewing prompts with GPT-specific behavior, API constraints, and migration references for the user-specified or detected runtime model. |

#### Research and Explanation

Source: `research/skills/`.

| Skill | Use it for |
| --- | --- |
| `explain-step-by-step` | Progressive, evidence-grounded mental models for complex material. |
| `ground-with-google-genai` | Grounded Google Search, Maps, and specific-URL research with Gemini. |

#### Slides and Visuals

Source: `visuals/skills/`.

| Skill | Use it for |
| --- | --- |
| `author-marp-slides` | Focused Marp/Marpit authoring, templates, themes, and rendered checks. |
| `create-mermaid-diagrams` | Editable Mermaid diagrams with optional consumer-ready SVG rendering. |
| `create-slide-decks` | Complete Marp decks with coordinated narrative, colors, visuals, and rendering. |
| `create-svg-illustrations` | Accessible, portable SVG diagrams and illustrations for target artifacts. |
| `design-slide-colors` | Semantic slide palettes with usage rules and measured contrast evidence. |

#### Planning and Experience Design

Source: `design/skills/`.

| Skill | Use it for |
| --- | --- |
| `design-user-experiences` | Design, review, or implement bounded interfaces and approval-gated end-to-end digital experiences. |
| `grill-designs` | Evidence-informed, one-decision-at-a-time design grilling. |
| `write-roadmap` | Creating, revising, reviewing, and tracking evidence-grounded strategic roadmaps, then deleting them when complete. |

#### Code Quality and Architecture

Source: `code-quality/skills/`.

| Skill | Use it for |
| --- | --- |
| `harden-code-paths` | Confirming and fixing code-path failure modes or verified security findings, with bounded same-pattern checks. |
| `improve-codebase-architecture` | Evidence-led codebase architecture assessment and behavior-preserving refactoring. |
| `review-code` | Evidence-led ordinary code review with baseline security checks and authorized hardening handoff. |

#### Project and Git Workflow

Source: `workflow/skills/`.

| Skill | Use it for |
| --- | --- |
| `use-jira-cli` | Read-only Jira inspection and precisely authorized CLI mutations. |
| `write-git-commits` | Drafting, validating, or creating focused Conventional Commits from diffs. |

### Saved UI Styles

Install the repository's saved styles from `skills/design/` with `npx skills`; `just install` includes them.
`curate-ui-styles` saves new styles to `~/.agents/skills/design/ui-style-<id>/SKILL.md` by default, after you confirm the destination.
To use a style, name it explicitly or ask the agent to read its `SKILL.md`.

| Skill | Use it for |
| --- | --- |
| [Minimalist](skills/design/ui-style-minimalist/SKILL.md) | Apply the Minimalist style to web app overviews and dashboards only when explicitly selected by name or path. |

### External Skills

External skills recorded in [`skills-lock.json`](skills-lock.json):

| Skill | Source repository |
| --- | --- |
| `chrome-extensions` | [GoogleChrome/modern-web-guidance][googlechrome-skills] |
| `correct` | [cursor/plugins][cursor-skills] |
| `modern-web-guidance` | [GoogleChrome/modern-web-guidance][googlechrome-skills] |
| `security-audit` | [cloudflare/security-audit-skill][cloudflare-skills] |

[googlechrome-skills]: https://github.com/GoogleChrome/modern-web-guidance
[cursor-skills]: https://github.com/cursor/plugins
[cloudflare-skills]: https://github.com/cloudflare/security-audit-skill

## 🗄️ Deprecated Skills

Retired skills are kept in `./deprecated/` for reference. `npx skills add`
does not discover them.

| Skill | Notes |
| --- | --- |
| `audit-code-security` | Legacy read-only security audit workflow; use `security-audit` for maintained security guidance and audits. |
| `checking-cli-help` | Legacy decision rule for focused command-help inspection. |
| `cleaning-atuin-history` | Legacy Atuin audit and exact-approval cleanup preparation. |
| `building-codex-hooks` | Version-sensitive legacy Codex CLI hook reference. |
| `writing-work-logs` | Legacy explicit-only Git-evidence work logs. |
| `naming-agent-skills` | Merged into `write-agent-skills`; retained as a compatibility reference. |
| `scoring-agent-skills` | Merged into `write-agent-skills`; retained as a compatibility reference. |
| `designing-user-interfaces` | Merged into `design-user-experiences`; retained as a compatibility reference. |
| `researching-gourmet-venues` | Rarely used city dining workflow retained as a compatibility reference. |
| `syncing-main-branch` | Legacy explicit-only main-branch synchronization workflow. |
| `iterating-ui-improvements` | Legacy explicit-only DevTools audit-fix-commit loop. |
| `building-typer-clis` | Legacy Typer-specific CLI workflow retained as a compatibility reference. |
| `configuring-python-logging` | Legacy Python logging configuration workflow retained as a compatibility reference. |
| `manage-python-with-uv` | Legacy uv project, script, and authorized publishing workflow retained as a compatibility reference. |
| `apply-tdd` | Legacy TDD workflow with production-path and test-isolation boundaries retained as a compatibility reference. |
| `using-peewee-orm` | Legacy Peewee lifecycle workflow retained as a compatibility reference. |
| `managing-git-worktrees` | Legacy loss-aware Git worktree lifecycle workflow retained as a compatibility reference. |
| `maintaining-memory-md` | Legacy repository memory curation workflow retained as a compatibility reference. |
| `resolving-pr-review-comments` | Legacy explicit PR feedback workflow; use `address-pr-feedback` for the active workflow. |
| `using-codebase-memory-cli` | Legacy CLI-only codebase graph workflow retained as a compatibility reference. |
| `running-panel-review-loops` | Legacy multi-reviewer code review and authorized fix loop retained as a compatibility reference. |
| `typesafe-ai` | Legacy TypeSafe System One integration workflow retained as a compatibility reference. |
