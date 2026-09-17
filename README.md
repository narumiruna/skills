# Skills

Reusable agent skills for coding, writing, research, and slide work. This repo is organized for Codex-first workflows and can also be installed as a standard skills repo.

## 🚀 Quick Start

Install the collection:

```shell
npx skills add narumiruna/skills
```

Then open Codex and run `/skills` to inspect what was installed. Invoke a skill explicitly with `$skill-name`, or describe the task normally and let Codex choose a match.

## 📦 Install

### Standard install with `npx skills`

Use this when you want the collection without linking a local checkout:

```shell
npx skills add narumiruna/skills
```

Standard discovery exposes active skills only; deprecated skills live outside `skills/` and remain available solely for repository reference or explicit local use.

### Local checkout with GNU Stow

Use this when you want `~/.agents/skills` to track a local checkout. Install [just](https://just.systems/) and [GNU Stow](https://www.gnu.org/software/stow/), then run:

```shell
just install
```

This links the repository's `skills/` directory to `~/.agents/skills`. Remove the managed link with:

```shell
just uninstall
```

## 🧭 How To Use In Codex

- Run `/skills` to inspect the installed collection.
- Type `$manage-python-with-uv`, `$apply-imrad`, or another skill name to invoke one explicitly.
- Describe the task normally and let Codex choose a matching skill.

If Codex does not pick up a local skill change, restart Codex and try again.

## 🧰 Skill Catalog

All active skills live directly under `skills/<skill-name>/`.

| Skill | Use it for |
| --- | --- |
| `apply-imrad` | Evidence-traceable IMRaD fit checks, reviews, transformations, and drafts. |
| `apply-tdd` | Scoping red-green-refactor with explicit production-path, test-data, and observable-behavior boundaries. |
| `audit-code-security` | Evidence-led, security-first, read-only code audits with verified findings and bounded tool use. |
| `author-marp-slides` | Focused Marp/Marpit authoring, templates, themes, and rendered checks. |
| `calibrate-writing-style` | Explicit-invocation interviews that refine reusable English and Taiwan Traditional Chinese writing-style prompts. |
| `create-agent-skills` | Creating, naming, reviewing, revising, and explicitly scoring lean, discoverable agent skills. |
| `create-mermaid-diagrams` | Editable Mermaid diagrams with optional consumer-ready SVG rendering. |
| `create-slide-decks` | Complete Marp decks with coordinated narrative, colors, visuals, and rendering. |
| `create-svg-illustrations` | Accessible, portable SVG diagrams and illustrations for target artifacts. |
| `create-telegraph-pages` | Preparing and publishing one explicitly authorized Telegra.ph article. |
| `design-slide-colors` | Semantic slide palettes with usage rules and measured contrast evidence. |
| `design-user-experiences` | Design, review, or implement bounded interfaces and approval-gated end-to-end digital experiences. |
| `explain-step-by-step` | Progressive, evidence-grounded mental models for complex material. |
| `grill-designs` | Evidence-informed, one-decision-at-a-time design grilling. |
| `ground-with-google-genai` | Grounded Google Search, Maps, and specific-URL research with Gemini. |
| `harden-code-paths` | Confirming and fixing code-path failure modes or verified security findings. |
| `improve-codebase-architecture` | Evidence-led codebase architecture assessment and behavior-preserving refactoring. |
| `manage-python-with-uv` | uv projects, scripts, dependencies, checks, builds, and authorized publishing. |
| `operate-ghostty` | Inspecting, launching, configuring, validating, and troubleshooting Ghostty. |
| `prompt-gpt` | Creating, revising, and reviewing prompts using references for the user-specified or detected runtime model, or general principles when unknown or not covered. |
| `review-code` | Evidence-led ordinary code review with baseline security checks and authorized hardening handoff. |
| `use-jira-cli` | Read-only Jira inspection and precisely authorized CLI mutations. |
| `write-agents-md` | Creating, reviewing, and automatically maintaining lean, evidence-backed `AGENTS.md` guidance at the narrowest applicable scope. |
| `write-git-commits` | Drafting, validating, or creating focused Conventional Commits from diffs. |
| `write-plans` | Drafting, executing, and tracking lean implementation plans with acceptance evidence, then deleting them when complete. |
| `write-roadmap` | Creating, revising, reviewing, and tracking evidence-grounded strategic roadmaps, then deleting them when complete. |

## 🗄️ Deprecated Skills

Deprecated skills remain in `deprecated/<skill-name>/` for reference and are excluded from standard discovery.

| Skill | Notes |
| --- | --- |
| `checking-cli-help` | Legacy decision rule for focused command-help inspection. |
| `cleaning-atuin-history` | Legacy Atuin audit and exact-approval cleanup preparation. |
| `building-codex-hooks` | Version-sensitive legacy Codex CLI hook reference. |
| `writing-work-logs` | Legacy explicit-only Git-evidence work logs. |
| `naming-agent-skills` | Merged into `create-agent-skills`; retained as a compatibility reference. |
| `scoring-agent-skills` | Merged into `create-agent-skills`; retained as a compatibility reference. |
| `designing-user-interfaces` | Merged into `design-user-experiences`; retained as a compatibility reference. |
| `researching-gourmet-venues` | Rarely used city dining workflow retained as a compatibility reference. |
| `syncing-main-branch` | Legacy explicit-only main-branch synchronization workflow. |
| `iterating-ui-improvements` | Legacy explicit-only DevTools audit-fix-commit loop. |
| `building-typer-clis` | Legacy Typer-specific CLI workflow retained as a compatibility reference. |
| `configuring-python-logging` | Legacy Python logging configuration workflow retained as a compatibility reference. |
| `using-peewee-orm` | Legacy Peewee lifecycle workflow retained as a compatibility reference. |
| `managing-git-worktrees` | Legacy loss-aware Git worktree lifecycle workflow retained as a compatibility reference. |
| `maintaining-memory-md` | Legacy repository memory curation workflow retained as a compatibility reference. |
| `resolving-pr-review-comments` | Legacy explicit PR feedback workflow retained as a compatibility reference. |
| `using-codebase-memory-cli` | Legacy CLI-only codebase graph workflow retained as a compatibility reference. |
| `running-panel-review-loops` | Legacy multi-reviewer code review and authorized fix loop retained as a compatibility reference. |
