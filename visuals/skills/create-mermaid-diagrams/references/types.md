# Mermaid Type Guidance

Use this reference only after choosing a diagram type. The basic `.mmd` files linked from `SKILL.md` are the editable syntax starting points; this file adds only type-specific decisions and non-obvious syntax.

## Flowchart

Use `TD` for vertical processes and `LR` for horizontal handoffs. Reserve diamonds for decisions, label consequential branches, and split a workflow that no longer fits one readable screen. Common node forms are `[process]`, `{decision}`, `((terminal))`, and `[(database)]`.

## Sequence

Name participants after roles or systems rather than implementation classes. Use `->>` for calls and `-->>` for responses. Add `alt`, `opt`, or `loop` only when the branch is essential, and keep one principal scenario per diagram.

## Class

Show only fields and methods needed for the discussion. Use cardinality where multiplicity matters and model interfaces only when they explain a real boundary. Relationship operators include `<|--` inheritance, `*--` composition, `o--` aggregation, and `..>` dependency.

## State

Use states for durable conditions rather than one-off actions. Label transitions when the trigger matters, keep terminal states explicit with `[*]`, and split concurrent or nested lifecycles before they obscure the allowed transitions.

## ER

Use entity names that match tables or domain nouns, and split large schemas by bounded context. Add attributes only when they clarify the relationship. Common cardinalities are `||--||` one-to-one, `||--o{` zero-or-many, `||--|{` one-or-many, and `}o--o{` many-to-many.

## Other Types

- **Gantt:** schedules and dependencies; verify date formats and dependency ordering.
- **Pie:** small part-to-whole breakdowns, not precise comparison across many values.
- **Git graph:** branch and release explanations.
- **Journey:** user steps and sentiment.
- **Quadrant:** two-axis prioritization.
- **Timeline:** chronological events.
- **Mindmap:** topic decomposition.
- **Requirement:** requirement traceability.
- **C4:** system context only when the target Mermaid renderer supports C4 syntax.

Check the target renderer before using version-sensitive or experimental diagram types.
