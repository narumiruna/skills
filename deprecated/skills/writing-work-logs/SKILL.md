---
name: writing-work-logs
description: Use only when the user explicitly names writing-work-logs to produce a concise, evidence-based Git work log for a resolved date range; never auto-activate for generic status or summary requests.
metadata:
  internal: true
---

# Writing Work Logs (Deprecated Reference)

Use only after explicit invocation. Operate on one repository and do not save a file unless requested.

## Workflow

1. Resolve the date range. Check the local date for relative terms; interpret “last week” as the previous calendar week unless context makes “last seven days” materially plausible. Ask for a range when none is provided.
2. Gather commits with hashes, dates, authors, and subjects. Identify the current Git user's name/email when filtering a multi-author history; ask only when ownership remains ambiguous.
3. Inspect `git show --stat` or `--name-only` when subjects do not support a reliable summary. For a range including today, inspect uncommitted status/diff only when useful and label it as in progress.
4. Use user notes as evidence but never invent completed work. Mark irreducible uncertainty or request the minimum missing context.
5. Return exactly:

```markdown
# Work Log - <concrete date range>

- <high-impact work item>
- <progress, blocker, or follow-up>
```

Keep one flat bullet list, ordered by likely team/customer impact, risk reduction, unblockers, and follow-ups before low-level implementation detail. Use concrete dates, not relative labels.
