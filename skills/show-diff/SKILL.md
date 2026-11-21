---
name: show-diff
description: Show changes or compare two named things when the user asks for a diff, patch, or before-and-after comparison. Default to a high-level Git-style diff for code, documents, or concepts such as algorithms. Expand details or show the actual patch when requested and available.
---

# Show Diff

## Resolve the comparison

1. Identify the two sides before comparing them.
   - For named concepts, products, or approaches, compare them in the order given under the same assumptions.
     State versions, variants, or defaults when they affect the comparison.
   - For repository changes, use the supplied diff or resolve the requested files, commits, or branches.
     - If no subjects or range are given, inspect staged, unstaged, and relevant untracked changes.
     - For changes proposed by a branch or open PR, compare the branches' common ancestor with the feature tip.
     - For a direct comparison of two branch snapshots, compare their tips.
     - For a merged PR, verify the target branch's state immediately before and after the merge, then compare those two states.
       Do not compare the PR head with the current target tip.
2. Report only supported differences and distinguish intended behavior from verified results where applicable.
   For a verified addition or deletion, treat the absent side as empty.
   If there are no material differences or required information is missing, say so.
3. Do not edit files, stage changes, or commit as part of showing the diff.

## Choose the level of detail

- For a plain request such as “show diff,” use the high-level summary below.
- For more detail, expand the requested parts.
  Use exact excerpts for file changes when useful and label them as partial.
  For a concept comparison, add concrete examples, formulas, or source details as relevant.
- For a raw diff, complete patch, or line-by-line comparison, show the actual diff for the requested scope without paraphrasing.
  Do not present an excerpt as complete or invent a patch when there are no files to compare.

## Format the high-level summary

- Label the output as a summary, not an apply-ready patch, and use one fenced `diff` block.
- For file changes, use `diff --git a/<old-path> b/<new-path>` with repository-relative paths.
  Show `rename from` and `rename to` only when the rename is established.
- For concepts, use `--- <first subject>` and `+++ <second subject>` instead of inventing Git paths.
- Group related differences under short labels such as `@@ Scope @@` or `@@ Workflow @@`, without line numbers.
- Use `-` and `+` for the first and second sides, respectively.
  In concept comparisons, these markers do not imply replacement or rank.
  Include an unmarked context line only when shared behavior helps explain a difference.
- Summarize the important changes in plain language.
  Preserve material conditions, exceptions, and compatibility effects; omit incidental wording and formatting edits.

## Add a visual when it helps

Honor requests for a specific format.
Otherwise, add a table or Mermaid diagram to the text diff only if it clarifies an important difference.

- Use a Markdown table to compare the same attributes, settings, or trade-offs side by side.
  Label differences in text instead of relying on color or icons alone.
- Use Mermaid to show changes to paths, dependencies, interaction order, or state transitions.
  Keep the diagram focused on the changed relationships, such as a new cache-hit path that skips the database.
- Do not repeat the full summary in another format or add a visual to a raw-patch-only response.

## Examples

The repository examples use fictional changes and generic identifiers.

### Current local changes

Request: “Show diff.”

High-level diff (summary, not a patch):

```diff
diff --git a/docs/setup.md b/docs/quickstart.md
rename from docs/setup.md
rename to docs/quickstart.md
@@ Setup @@
- Ask readers to edit the configuration before the first run.
+ Start with defaults and document configuration as optional.
```

### Changes proposed by a branch

Request: “Show what `feature/export` adds to `origin/main` for the PR.”

`origin/main...feature/export` (summary, not a patch):

```diff
diff --git a/docs/export.md b/docs/export.md
@@ Export formats @@
- Export supports CSV only.
+ Export also supports JSON.
```

### Actual changes after a PR merges

Request: “What changed on the target branch when this PR merged?”
For a verified merge commit `M` on the target branch, compare `M^1` with `M`.

Target branch before → after (summary, not a patch):

```diff
diff --git a/config/retention.conf b/config/retention.conf
@@ Log retention @@
- Keep all logs for 7 days.
+ Keep application logs for 30 days; audit logs still expire after 7 days.
```

### Follow-up asking for exact lines

Request: “Show the exact lines for log retention.”

Partial diff (`config/retention.conf` only):

```diff
@@ -3 +3,2 @@
-log_days=7
+application_log_days=30
+audit_log_days=7
```

For “Show the full raw patch,” show the complete actual diff for the same comparison, not this excerpt.

### Comparing two algorithms

Request: “Show diff between Adam and RMSProp.”

Concept comparison (original Adam vs. basic RMSProp without optional momentum):

```diff
--- Adam
+++ RMSProp
@@ Gradient used for the step @@
- Uses a moving average of gradients before per-parameter scaling.
+ Uses the current gradient before per-parameter scaling.

@@ Moving averages @@
  Both track a moving average of squared gradients to scale each parameter's step.
- Corrects the initial bias of both moving averages.
+ Does not apply Adam-style bias correction.
```

### Comparing two systems of government

Request: “Show diff between a parliamentary system and a presidential system.”

Concept comparison (typical systems; constitutional details vary):

```diff
--- Parliamentary system
+++ Presidential system
@@ Government leadership @@
- A prime minister leads the government, which depends on the legislature's confidence.
+ A separately elected president leads the executive without needing the legislature's confidence to stay in office.

@@ Early removal @@
- A vote of no confidence can bring down the government.
+ Loss of legislative support alone does not end the president's fixed term; early removal follows a separate constitutional process.
```
