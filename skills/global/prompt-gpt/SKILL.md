---
name: prompt-gpt
description: Create, revise, or review prompts and agent instructions using GPT-specific behavior, API constraints, and migration references for the user-specified or detected runtime model.
---

# Prompting GPT

## Select Model Guidance

- Use the model explicitly specified by the user; otherwise, detect the current model from trusted runtime metadata, such as `PI_MODEL` when provided by the host.
- Do not infer model identity from the assistant's self-description or substitute an application's configured model for the runtime model.
- If the selected model is covered by a [model reference](#model-guides), read that guide first, accepting aliases or families only when the guide explicitly covers them.
- If detection fails or no reference covers the selected model, do not load another model's guide or add model-specific assumptions.

## Model Guides

When updating model references, consult the [official latest-model documentation](https://developers.openai.com/api/docs/guides/latest-model) to find current model, migration, and prompting guides.

Available references:

- [GPT-5.4](references/gpt-5.4.md)
- [GPT-5.5](references/gpt-5.5.md)
- [GPT-5.6](references/gpt-5.6.md)
- [GPT-6 family](references/gpt-6.md): `gpt-6-astra`, `gpt-6.1-sol`, `gpt-6.1-terra`, `gpt-6-luna`, and `gpt-6-sol`.

For current GPT-6 work, use the family guide.
The [earlier GPT-6 Astra reference](references/gpt-6-astra.md) is retained for comparison.

For Programmatic Tool Calling, confirm support in the selected guide before consulting the [API and output notes](references/gpt-5.6.md#programmatic-tool-calling).
