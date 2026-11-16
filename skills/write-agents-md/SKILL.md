---
name: write-agents-md
description: Create, review, audit, migrate, or update scoped AGENTS.md files with clear rules, verified commands, action limits, instruction order, and checks that prove the work is done. Use also when verified, durable repository guidance emerges during authorized work and should be captured at the narrowest applicable scope.
---

# Writing AGENTS.md

Write the shortest useful repository guide.
Give the agent the context, limits, authority, and evidence needed to finish the work safely.

## Workflow

- Find the target directory and every `AGENTS.md` file that applies to it.
  - Follow explicit user instructions before repository instructions.
  - Treat each file as applying to its directory subtree, with the closest scoped file before its parent files.
  - Put shared guidance at the narrowest common parent scope.
  - Use one root file by default.
  - Add nested files only when a subproject needs different rules.
- Inspect the current guidance, human docs, configuration, task files, CI, and relevant package docs.
  - Verify commands and paths from files that tools can run or read.
  - Find files that are generated or copied from elsewhere.
  - Find risky migrations, destructive steps, external actions, large data, and ownership rules that change how the agent should work.
- Keep only correct, project-specific rules.
  - Remove stale, repeated, guessed, generic, or misplaced content.
  - Keep shared rules in parent files and local differences in child files.
- Check the instruction chain for conflicts.
  - Run checks that match the size and risk of the change.
  - Inspect the diff for repeated rules or extra scope.
  - Label facts that you could not verify.
- For reviews, check wrong commands, stale paths, conflicting scope, unsafe permissions, and missing checks first.
  - Give each finding a severity, location, evidence, and replacement.
  - If no findings remain, say so and name any important missing evidence.

## Automatic Maintenance

Outside an explicit request to edit `AGENTS.md`, capture guidance only when repository evidence proves a durable, repository-specific rule that will change future agent work.
Do not record task history, transient status, speculation, generic advice, secrets, or guidance already owned by authoritative documentation.
Do not create `AGENTS.md` merely because it is absent.
When qualifying guidance emerges during authorized repository changes, update or create the file at the narrowest applicable directory scope.
During answer, review, diagnosis, or planning work, report the candidate rule instead of writing it.
Place the rule in the matching existing section, or add a relevant default section only when the evidence justifies it.
Prefix each automatically added or materially rewritten rule with `[UNREVIEWED]`:

```markdown
- [UNREVIEWED] Run `pnpm test:web` after changing this package.
```

Treat marked rules as active instructions; the marker records user-review status, not uncertainty or reduced authority.
Remove the marker only at the user's explicit direction.
Keep it when rewording or merging marked guidance, and do not add it to an equivalent rule the user has already reviewed.
Merge or revise overlapping marked rules instead of appending duplicates.
During incidental maintenance, do not silently rewrite or remove an unmarked rule; report contradictory evidence unless the user requested `AGENTS.md` maintenance.
After editing, reread the applicable instruction chain and verify scope, placement, deduplication, marker preservation, and absence of sensitive or task-log content.
Report only the automatically maintained rules that changed.

## Templates

Read the [section and action-policy templates](references/templates.md) when creating or restructuring a guide, or when adding an action policy.
For bounded edits and reviews, load only a relevant template instead of the full checklist.

## Writing Rules

- Organize rules under descriptive `##` section headings and write each rule as a concise, enforceable, one-sentence bullet list item.
- State the outcome, useful context, hard limits, actions that need approval, and success criteria.
- Describe a sequence only when its order matters.
- State each rule once in the smallest scope where it belongs.
- Use direct wording and exact paths, commands, conditions, evidence, and stopping points.
- Include only the scope, commands, code and test conventions, security or data limits, and collaboration or release rules that an agent needs.
- Keep product descriptions and human walkthroughs in human docs.
- Keep examples or writing-style rules only when they encode a project requirement or prevent a demonstrated mistake.
- Name unclear points that require a question.
- Do not require blanket approval for safe local work.

Add automation rules only for workflows the repository uses.
For small automation workflows, define the stage, allowed tools, required evidence, limits, and stopping point.
State when judgment or approval must take over.
