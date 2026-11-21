---
name: show-diff
description: Compare two or more subjects when the user asks to compare them, asks how they differ, or asks which to choose between them. Plain requests such as “compare Python and Rust” count; no format or diff keyword is required. Also use to show Git changes, PR comparisons, or raw patches. Choose a Git-style summary, table, or Mermaid diagram based on the comparison unless the user requests a format.
---

# Show Diff

## Resolve the comparison

1. Identify what the user wants to compare.
   - For concepts, products, or approaches, compare the subjects in the order given under the same assumptions.
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
3. Keep comparisons read-only except for the preference updates defined below.
   Do not stage, commit, or push those updates.

## Choose the format and level of detail

Honor the user's requested format.
If a follow-up only changes the format, keep the same subjects and scope.
Otherwise, use the most specific matching confirmed preference from [preferences.md](references/preferences.md) in this skill directory.
If no confirmed preference clearly applies, choose one primary format:

- Use a high-level Git-style diff for a bare “show diff” request, repository changes, or a before-and-after comparison.
  Also use it for two subjects with a few clear contrasts that read well as `-` and `+` pairs.
- Use a Markdown table when readers need to scan the same attributes or trade-offs across alternatives.
  Put one comparison criterion per row and one subject per column.
  Label differences in text instead of relying on color or icons alone.
- Use Mermaid when the key difference is easier to see as a path, dependency, interaction order, or state transition.
  Focus on the relationships that differ and state the main takeaway in text.

Unless the user asks for both formats, add a second format only if it clarifies an important difference without repeating the full comparison.
For more detail, expand the requested parts with exact excerpts, examples, formulas, or source details as useful.
Label diff excerpts as partial.
For a raw diff, complete patch, or line-by-line file comparison, show the actual diff for the requested scope without paraphrasing or adding visuals.
Do not present an excerpt as complete or invent a patch when there are no files to compare.

## Remember format preferences by comparison type

Update only the skill's [preference file](references/preferences.md), not a copy in the repository being compared.
Save only the comparison type and primary format: Git-style summary, Markdown table, or Mermaid.
Omit subject names, raw patches, quotes, and conversation details.

- When the user asks to switch the current comparison's primary format, apply it and save it as a candidate for that type.
  Leave the confirmed default unchanged, even if the user requests the same switch again.
- When the user explicitly sets a default for a type, save it as confirmed and clear the candidate.
- Do not save a preference if the request is one-time, applicable rules prohibit writes, only the level of detail changes, or the comparison type is unclear.

Reuse an existing type when it fits; add a narrower row when the user states a distinct preference.
If the file cannot be updated, apply the requested format without saving it.
When a preference changes, briefly say what was recorded so the user can review it in Git.

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

### Comparing alternatives across shared criteria

Request: “Compare Python and Rust.”

| Criterion | Python | Rust |
| --- | --- | --- |
| Type checking | Dynamic by default; optional type hints can be checked with separate tools. | Static; the compiler checks types before the program runs. |
| Memory management | The runtime manages object lifetimes automatically. | Ownership and borrowing rules are checked at compile time. |
| Typical uses | Automation, data analysis, and prototyping. | Native CLI tools, system components, and performance-sensitive services. |

### Comparing two algorithms in diff format

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
