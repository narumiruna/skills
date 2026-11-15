---
name: maintaining-memory-md
description: Deprecated internal reference for reading, maintaining, and curating concise repository-root MEMORY.md notes for verified gotchas, durable user preferences, and established repository conventions.
metadata:
  internal: true
---

# Maintaining MEMORY.md (Deprecated Reference)

This workflow is excluded from active discovery but retained for repository reference and explicit local compatibility.
Resolve the repository root and inspect `MEMORY.md` at the start of repository work and before non-trivial debugging, design, workflow, or skill maintenance.
Missing memory is normal.
Current repository evidence always overrides it.
All memory writes, including curation of existing entries, require write authority for the current task.
During read-only or plan-only work, report proposed curation or new entries instead of changing memory.

## Qualifying Entries

- **GOTCHA:** repository evidence proves a reusable trap or failure mode and its cause, recovery, or avoidance is known.
- **TASTE:** the user expresses a durable preference that will change future repository work.
- **CONVENTIONS:** repository evidence proves a stable, repository-specific pattern in code, structure, naming, testing, or workflow that will change future work.

Do not record transient status, task history, broad summaries, speculation, generic best practices, or secrets. Do not add conventions already stated in `AGENTS.md` or authoritative documentation. If a convention should govern all contributors, recommend updating its authoritative owner unless that file is already within the user's requested scope; do not add a new memory entry for it. During curation, retain an existing entry that is the sole record until its authoritative update is completed, then remove the duplicate. Sanitize any reusable lesson involving credentials, tokens, private endpoints, proprietary data, or personal information.

## Curate

During authorized repository changes, perform lightweight curation when inspecting or updating memory.
Using the evidence already gathered, merge, revise, remove, or sanitize entries that are demonstrably duplicated, misplaced, contradicted, stale, non-qualifying, or sensitive.
Do not broaden a lightweight pass into a repository-wide audit.

When writes are authorized, perform full curation if the user requests it or concrete evidence suggests `MEMORY.md` may be stale.
Check every entry against current repository evidence, authoritative guidance, and later explicit user preferences:

- Keep entries that remain correct and qualifying.
- Merge or rewrite entries that remain useful but are inaccurate, misplaced, or overlapping.
- Remove or safely rewrite entries proven wrong, stale, superseded, duplicated, non-qualifying, or sensitive.
- Leave an entry unchanged when it cannot currently be reverified and no evidence contradicts it. Report it as unverified; absence of evidence is not evidence that it is stale.

## Create or Update

- Do not create `MEMORY.md` merely because it is absent.
- When the first qualifying entry emerges and repository writes are authorized, create the root file without asking solely about its absence.
- Keep exactly these top-level sections:

```markdown
## GOTCHA

## TASTE

## CONVENTIONS
```

- Add one concise bullet under the matching section. Revise a similar, stale, wrong, or contradicted entry instead of appending a duplicate.
- Keep entries grounded in reusable repository behavior:

```markdown
- Symptom: <failure>. Cause: <reason>. Fix: <future action>.
- Prefer <choice> when <context>; avoid <alternative> because <reason>.
- Use <pattern> for <context>; repository evidence: <concise evidence>.
```

After editing, reread the file to verify all three headings, placement, deduplication, and absence of sensitive or task-log content. For an ordinary update or lightweight pass, report only entries actually changed. For full curation, summarize kept, merged or revised, removed or sanitized, and unverified entries. Do not claim edits or verification that were not completed.
