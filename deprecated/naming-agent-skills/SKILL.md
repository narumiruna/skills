---
name: naming-agent-skills
description: Deprecated compatibility reference for choosing, reviewing, renaming, or standardizing agent skill names. Use the active write-agent-skills workflow for current naming and authorized repository rename work.
metadata:
  internal: true
---

# Naming Agent Skills (Deprecated Reference)

Use `write-agent-skills` for the maintained workflow. This reference preserves the former `$naming-agent-skills` behavior for explicit local use.

Name the task and trigger the skill represents, not its implementation.

## Rules

- Use lowercase kebab-case: letters, meaningful digits, and single hyphens; no leading or trailing hyphen.
- Prefer two to four specific words and stay within the target framework's length limit.
- Avoid vague words such as `helper`, `utils`, `tools`, `assistant`, `magic`, `smart`, `general`, `data`, `files`, or `documents`.
- Avoid product or organization names unless the trigger is genuinely product-specific.
- Prefer user intent over implementation detail and a name that remains valid if internals change.
- Inspect sibling names and references; minimize overlap with existing triggers.

Use `<verb-ing>-<object>` as a useful default, not a mandate. Preserve the skill's original meaning when another pattern is clearer or the library has an established convention. Domain-first or command-style names are valid when they match the surrounding collection.

## Selection

1. Read the skill's actual description and workflow; do not name from an informal label alone.
2. Identify the triggering action, object or domain, and any necessary product qualifier.
3. Generate a small set of candidates in the repository's naming style.
4. Compare candidates for specificity, searchability, future stability, and collision risk.
5. Recommend one name with the deciding reason and mention alternatives only when they represent a real tradeoff.

Prefer `analyzing-test-results` over `parse-json`, and `adding-message-timestamps` over a product-prefixed name unless the behavior is product-specific.

## Rename Boundary

Distinguish a naming recommendation from a requested repository rename. Do not edit files when the user asked only for names or review.

For an authorized rename, use the skill-maintenance workflow and update the directory, frontmatter `name`, catalog, links, examples, tests, and other exact-name references as one bounded change. Preserve compatibility notes when external consumers depend on the old name, then run repository validation.

## Output

Lead with the recommendation or verdict and its brief reason. For multiple skills, use a current/recommended/reason table. Include conflicts or compatibility work that would affect adoption; omit formulaic alternatives and repeated rules.
