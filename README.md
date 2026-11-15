# Skills

Reusable agent skills for coding, writing, research, and slide work. This repo is organized for Codex-first workflows and can also be installed as a standard skills repo.

## 🚀 Quick Start

Install the collection:

```shell
npx skills add narumiruna/skills/skills
npx skills add narumiruna/skills/optional/skills
```

Then open Codex and run `/skills` to inspect what was installed. Invoke a skill explicitly with `$skill-name`, or describe the task normally and let Codex choose a match.

## 📦 Install

### Standard install with `npx skills`

Use this when you want the collection without linking a local checkout:

```shell
npx skills add narumiruna/skills/skills
npx skills add narumiruna/skills/optional/skills
```

These commands discover active skills from `skills/` and `optional/skills/` separately; deprecated skills live in `deprecated/` and remain available solely for repository reference or explicit local use.

### Local checkout with GNU Stow

Use this when you want `~/.agents/skills` to track a local checkout. Install [just](https://just.systems/) and [GNU Stow](https://www.gnu.org/software/stow/), then run:

```shell
just install
```

This links each skill in `skills/` directly into `~/.agents/skills/`. Skills in `optional/skills/` remain available for selective installation but are not linked by this recipe. Remove the managed links with:

```shell
just uninstall
```

Before updating an existing Stow installation after a source-directory move, run `just uninstall` from the old checkout, then update the checkout and run `just install`.

## 🧭 How To Use In Codex

- Run `/skills` to inspect the installed collection.
- Type `$review-code`, `$apply-imrad`, or another skill name to invoke one explicitly.
- Describe the task normally and let Codex choose a matching skill.

If Codex does not pick up a local skill change, restart Codex and try again.

## 🧰 Skill Catalog

### Global Skills

Global skills live under `skills/<skill-name>/` and are linked by `just install`.

| Skill | Use it for |
| --- | --- |
| `apply-google-style` | Writing, refactoring, and reviewing code and documentation with all guides in Google's style guide index. |
| `configure-ghostty` | Configuring, validating, diagnosing, and operating Ghostty with version-aware file, keybinding, runtime, and launch guidance. |
| `give-language-feedback` | Proactive, one-sentence grammar or wording feedback in any language alongside the main task, without requiring a language-help request. |
| `lean-verify` | Formalizing claims and constructing or checking Lean 4 proofs for mathematical theorems, program properties, algorithm correctness, and other formal-verification tasks in `~/.agents/lean`. |
| `prompt-gpt` | Creating, revising, and reviewing prompts with GPT-specific behavior, API constraints, and migration references for the user-specified or detected runtime model. |
| `record-human-feedback` | Recording human corrections, tool or workflow preferences, and follow-up explanation or simplification requests in `~/.agents/human-feedback/`, with response context and frequency summaries. |
| `write-agent-skills` | Creating, naming, renaming, reviewing, revising, and explicitly scoring lean, discoverable agent skills. |
| `write-agents-md` | Creating, reviewing, and automatically maintaining lean, evidence-backed `AGENTS.md` guidance at the narrowest applicable scope. |
| `write-plans` | Drafting, executing, and tracking agent-executable implementation plans with completion evidence and separate external handoff, then deleting completed plans. |

The former `create-agent-skills` skill is now named `write-agent-skills`.
The former `apply-google-rust-style` and `apply-google-typescript-style` skills are merged into `apply-google-style`.

### Optional Skills

Optional skills live under `optional/skills/<skill-name>/` and remain available for selective installation.

| Skill | Use it for |
| --- | --- |
| `apply-asd-ste100` | Drafting, revising, and reviewing technical documentation with ASD-STE100 rule and vocabulary checks for the requested issue (Issue 9 by default), or clarity principles without a compliance claim. |
| `apply-imrad` | Evidence-traceable IMRaD fit checks, reviews, transformations, and drafts. |
| `author-marp-slides` | Focused Marp/Marpit authoring, templates, themes, and rendered checks. |
| `calibrate-writing-style` | Explicit-invocation interviews that refine reusable English and Taiwan Traditional Chinese writing-style prompts. |
| `create-mermaid-diagrams` | Editable Mermaid diagrams with optional consumer-ready SVG rendering. |
| `create-slide-decks` | Complete Marp decks with coordinated narrative, colors, visuals, and rendering. |
| `create-svg-illustrations` | Accessible, portable SVG diagrams and illustrations for target artifacts. |
| `create-telegraph-pages` | Preparing and publishing one explicitly authorized Telegra.ph article. |
| `design-slide-colors` | Semantic slide palettes with usage rules and measured contrast evidence. |
| `design-user-experiences` | Design, review, or implement bounded interfaces and approval-gated end-to-end digital experiences. |
| `explain-step-by-step` | Progressive, evidence-grounded mental models for complex material. |
| `grill-designs` | Evidence-informed, one-decision-at-a-time design grilling. |
| `ground-with-google-genai` | Grounded Google Search, Maps, and specific-URL research with Gemini. |
| `harden-code-paths` | Confirming and fixing code-path failure modes or verified security findings, with bounded same-pattern checks. |
| `improve-codebase-architecture` | Evidence-led codebase architecture assessment and behavior-preserving refactoring. |
| `review-code` | Evidence-led ordinary code review with baseline security checks and authorized hardening handoff. |
| `use-jira-cli` | Read-only Jira inspection and precisely authorized CLI mutations. |
| `write-git-commits` | Drafting, validating, or creating focused Conventional Commits from diffs. |
| `write-roadmap` | Creating, revising, reviewing, and tracking evidence-grounded strategic roadmaps, then deleting them when complete. |

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

Deprecated skills remain in `deprecated/<skill-name>/` for reference and are excluded from standard discovery.

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
| `resolving-pr-review-comments` | Legacy explicit PR feedback workflow retained as a compatibility reference. |
| `using-codebase-memory-cli` | Legacy CLI-only codebase graph workflow retained as a compatibility reference. |
| `running-panel-review-loops` | Legacy multi-reviewer code review and authorized fix loop retained as a compatibility reference. |
| `typesafe-ai` | Legacy TypeSafe System One integration workflow retained as a compatibility reference. |
