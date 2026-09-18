---
name: prompt-gpt
description: Create, revise, or review prompts and agent instructions using the user-specified model or otherwise the detected runtime model to select a matching reference, with general principles only when the model is unknown or not covered.
---

# Prompting GPT

Produce the smallest prompt that preserves the product contract.

## Select Model Guidance

- Use the model explicitly specified by the user; otherwise, detect the current model from trusted runtime metadata, such as `PI_MODEL` when provided by the host.
- Do not infer model identity from the assistant's self-description or substitute an application's configured model for the runtime model.
- If the selected model is covered by a [model reference](#model-guides), read that guide first, accepting aliases or families only when the guide explicitly covers them.
- If detection fails or no reference covers the selected model, use only the general principles below, without loading another model's guide or assuming its API capabilities.

## Establish the Contract

- Inspect the existing prompt, relevant skills, `AGENTS.md` files, tool descriptions, API settings, representative tasks, and known failures before revising an established workflow.
- Identify duplicate or conflicting instructions across those sources and resolve conflicts according to the host's instruction hierarchy, preserving higher-priority requirements.
- Ask one narrow question only when missing context would materially change the artifact or create meaningful risk.
- Define the goal, relevant context, success criteria, constraints, evidence requirements, output expectations, and stopping conditions.
- Describe the required outcome and let the model choose the path unless sequence, method, or approval order is itself a product requirement.
- Use absolute rules only for true invariants, required fields, safety limits, or forbidden actions.
- Keep API configuration outside prompt prose when a dedicated parameter or Structured Output can enforce it.

## Bound Actions and Tool Use

- State safe autonomous actions and approval boundaries once.
- Allow in-scope, reversible local work without unnecessary confirmation and carry it through completion or an explicit blocker.
- Require approval before external writes, destructive or costly actions, purchases, or material scope expansion.
- Name the exact side effects an authorization permits, and do not infer related mutations.
- Expose only tools relevant to the task.
- Put tool-specific purpose, inputs, return shape, side effects, retry safety, and error behavior in the tool description.
- Keep only cross-tool routing, authorization, evidence, and stopping policy in the main prompt.
- Choose tool orchestration by task dependencies, required judgment, and approval boundaries rather than tool availability alone.
- For multi-agent workflows, define when to delegate independent work, each subagent's scope and expected result, concurrency limits, and who validates and integrates the results.
- For long-running workflows, define how to preserve completed actions, relevant assumptions, IDs, tool outcomes, blockers, and the next goal across continuation, compaction, or handoffs.

## Control Evidence and Output

- Define which claims need support, what evidence is sufficient, and how to report missing or conflicting evidence.
- Add a finite retrieval budget for grounded workflows, and permit another search only when a required fact, source, or comparison is still missing.
- Do not turn missing evidence into a factual negative.
- When the target API supports a verbosity setting, use it for the default detail level and prompt prose only for task-specific length, structure, audience, and required content.
- For short answers, preserve the conclusion, necessary evidence, material caveats, and next action before trimming background or repetition.
- Define tone through observable writing choices instead of broad labels such as “friendly” or “professional.”
- Request a visible preamble only when a streaming, multi-step workflow benefits from progress feedback.

## Remove Prompt Noise

- State each instruction once.
- Remove legacy step-by-step scaffolding, duplicated rules, generic background, and examples that do not encode a product requirement or correct a measured failure.
- Keep stable reusable instructions before dynamic request data when prompt caching matters.
- Do not ask the model to “think harder,” simulate Pro mode, or expose hidden reasoning.
- Do not include the current date unless the workflow needs a specific business, policy, or user-local date or timezone.
- Change one instruction group at a time when optimizing an existing prompt so evaluation results remain attributable.

## Validate the Result

- Test representative normal cases plus material ambiguity, missing evidence, denied side effects, tool failure, and stopping behavior when those risks apply.
- Compare task success, answer completeness, required evidence, total tokens, latency, and cost against the current prompt or a documented baseline.
- Tune supported reasoning settings on representative tasks unless the application fixes them, and increase effort only when measured quality gains justify added latency and cost.
- Run checks appropriate to the change and complete required validation; once those pass, broaden or repeat verification only for new changes, failures, or unresolved concerns.
- Treat fewer tokens, calls, or turns as an improvement only when the output still meets the quality bar.
- Do not claim improvement without representative evaluation evidence.

For review-only requests, keep the work read-only and lead with behavior-changing findings tied to exact prompt sections.
For create or revision requests, return the finished prompt first, then list separate API-setting recommendations, assumptions, and validation gaps only when they affect adoption.

## Model Guides

When updating model references, consult the [official latest-model documentation](https://developers.openai.com/api/docs/guides/latest-model) to find current model, migration, and prompting guides.

Available references:

- [GPT-5.4](references/gpt-5.4.md)
- [GPT-5.5](references/gpt-5.5.md)
- [GPT-5.6](references/gpt-5.6.md)
- [GPT-6 Astra](references/gpt-6-astra.md)

Use the selected guide for model-specific prompting, API compatibility, supported settings, and migration steps.
For Programmatic Tool Calling, confirm support in the selected guide before consulting the [routing and validation guidance](references/gpt-5.6.md#programmatic-tool-calling).
