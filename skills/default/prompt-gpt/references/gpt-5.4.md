# Using GPT-5.4

Source: condensed from the [official GPT-5.4 guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4).

## Models and Parameters

This reference covers [`gpt-5.4`](https://developers.openai.com/api/docs/models/gpt-5.4), [`gpt-5.4-pro`](https://developers.openai.com/api/docs/models/gpt-5.4-pro), [`gpt-5.4-mini`](https://developers.openai.com/api/docs/models/gpt-5.4-mini), and [`gpt-5.4-nano`](https://developers.openai.com/api/docs/models/gpt-5.4-nano).
The parameter notes below apply to `gpt-5.4`; do not assume identical settings for every variant.

- `reasoning.effort` supports `none`, `low`, `medium`, `high`, and `xhigh`, with `none` as the default.
- `text.verbosity` supports `low`, `medium`, and `high`, with `medium` as the default.
- At `medium` or `high` verbosity, GPT-5.4 tends to generate longer code with inline explanations; `low` produces shorter code with less commentary.
- `temperature`, `top_p`, and `logprobs` are supported only with reasoning effort set to `none`; other effort settings reject these fields.
- GPT-5.2 has the same restriction; older models such as `gpt-5`, `gpt-5-mini`, and `gpt-5-nano` reject those fields.

In Responses, use `reasoning.effort` and `text.verbosity`; in Chat Completions, use `reasoning_effort` and `verbosity`.
The [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses) can preserve reasoning context between turns; Chat Completions cannot pass that context.

## Context Window

GPT-5.4 supports up to a 1M-token context window.
[Pricing](https://developers.openai.com/api/docs/pricing) and [rate limits](https://developers.openai.com/api/docs/models/gpt-5.4) differ for requests below and above 272K tokens.
In [Fast mode](https://developers.openai.com/api/docs/guides/fast-mode), prompts above 272K tokens are processed at standard rates.
Long-context pricing stacks with data-residency and batch modifiers.

## Tools and State

- [Tool search](https://developers.openai.com/api/docs/guides/tools-tool-search) supports deferred loading of function, namespace, and MCP tool definitions.
- [Built-in computer use](https://developers.openai.com/api/docs/guides/tools-computer-use) returns structured actions for the application to execute from screenshots.
- [Custom tools](https://developers.openai.com/api/docs/guides/function-calling) use `type: "custom"` for raw-text input and can constrain it with a Lark context-free grammar.
  Responses places the custom tool's `name` and `description` directly on the tool; Chat Completions nests them under `custom`.
- `tool_choice` with `type: "allowed_tools"` restricts the model to a subset of the declared tools.
  Its `auto` mode permits a call from that subset; `required` requires one.
- [Compaction](https://developers.openai.com/api/docs/guides/compaction) returns opaque `encrypted_content` state for future requests and is compatible with Zero Data Retention.
  Keep prompts functionally identical after compaction.
  See the [`/responses/compact` API reference](https://developers.openai.com/api/reference/resources/responses/methods/compact).

### Phase Parameter

For long-running or tool-heavy Responses workflows, missing or dropped assistant `phase` values can make GPT-5.4 treat intermediate updates as final answers and stop early.
The field is optional at the API level but recommended for these workflows.
Use `phase: "commentary"` for intermediate assistant updates and `phase: "final_answer"` for the completed answer.
Do not add `phase` to user messages.
`previous_response_id` preserves prior assistant state; when replaying assistant history manually, preserve each original `phase` value unchanged.
See the [official phase guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.4#phase-parameter).

## Behavior Caveats

- Early-session tool routing can be less reliable when context is thin.
- GPT-5.4 can skip prerequisite lookups when the intended final action seems obvious.
- In long-running workflows, it can stop after partial coverage or treat empty or narrow retrieval as final.
- GPT-5.4 can overuse structured formatting and bullet lists.
- `none` can work well for action selection and tool discipline, but implicit requirements, ambiguity, and cancelled-tool-call recovery can need `low` or `medium`.

### Image Detail

For GPT-5.4 vision and computer use, select image detail explicitly when visual precision matters rather than relying on `auto`.
Use `high` for standard high-fidelity understanding, `original` for large or dense images, OCR, localization, and click accuracy, and `low` when fine detail is not needed.
See [Images and vision](https://developers.openai.com/api/docs/guides/images-vision).

### Smaller Models

`gpt-5.4-mini` and `gpt-5.4-nano` are less likely than larger models to infer missing steps, resolve ambiguity, or infer the intended output packaging.

- `gpt-5.4-mini` is more literal, makes fewer assumptions, and can add a follow-up question by default.
- For mini tool workflows, distinguish executing an action from reporting it and specify the required execution order.
- Scope mini instructions such as `output nothing else` to the final output, for example `after the final JSON, output nothing further`.
- Limit `gpt-5.4-nano` to narrow tasks with closed outputs such as labels, enums, or short JSON.
- Avoid nano for multi-step orchestration unless the flow is tightly constrained; use a stronger model for ambiguous or planning-heavy tasks.

## Migration Starting Points

| Current model | GPT-5.4 starting point |
| --- | --- |
| `gpt-5.2` | `gpt-5.4` with the current reasoning effort |
| `gpt-5.3-codex` | `gpt-5.4` with the current reasoning effort for coding workflows |
| `o3` | `gpt-5.4` with `medium`, then `high` if needed |
| `gpt-4.1` or `gpt-4o` | `gpt-5.4` with `none` |
| `o4-mini` or `gpt-4.1-mini` | `gpt-5.4-mini` |
| `gpt-4.1-nano` | `gpt-5.4-nano` |

For API details, see the [GPT-5 parameters and tools guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_new_params_and_tools) and [reasoning-state guidance](https://developers.openai.com/cookbook/examples/responses_api/reasoning_items).
