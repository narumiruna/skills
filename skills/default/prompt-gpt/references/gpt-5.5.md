# Using GPT-5.5

Source: condensed from the [official GPT-5.5 guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5).

## Migration and Behavior

Do not treat migration from `gpt-5.2` or `gpt-5.4` to `gpt-5.5` as a drop-in replacement.
GPT-5.5 follows instructions literally and thoroughly; detailed legacy process instructions can overconstrain its solution path or produce mechanical answers.
Its default style is concise, direct, and task-oriented, so conversational products may need explicit warmth or rationale.
GPT-5.5 coding agents can need explicit orchestration for reuse and subagent delegation.
GPT-5.5 may reason or prepare tool calls before emitting visible text; a short preamble can reduce perceived delay in streaming applications.
GPT-5.5 already knows the current UTC date; explicit date context is needed only for a different reference point, such as a user-local date or policy-effective date.

## Reasoning and Verbosity

- `reasoning.effort` supports `none`, `low`, `medium`, `high`, and `xhigh`, with `medium` as the default.
- For latency-sensitive tool use, planning, search, or multi-step decisions, evaluate `low` before `none`.
- Reserve `none` for latency-critical tasks that do not need reasoning or chained tool calls.
- Higher effort can cause overthinking, unnecessary search, or output regressions when instructions conflict, stopping criteria are weak, or tool access is open-ended.
- `text.verbosity` defaults to `medium`; `low` produces proportionally more concise responses than `low` on GPT-5.4.

See [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning) for setting details.

## Image Detail

- When `image_detail` is unset or `auto`, GPT-5.5 uses `original` behavior, preserving images without resizing up to 10,240,000 pixels or a 6,000-pixel dimension limit.
- Explicit `high` preserves images without resizing up to 2,500,000 pixels or a 2,048-pixel dimension limit.
- `low` resizes images above a 512-pixel dimension limit more aggressively than previous models.

See [Images and vision](https://developers.openai.com/api/docs/guides/images-vision).

## API and Conversation State

Use the [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses) for GPT-5.5 reasoning, tool calling, and multi-turn workflows.
GPT-5.5 retains GPT-5.4 API features, including [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching), [hosted tools](https://developers.openai.com/api/docs/guides/tools#available-tools), [tool search](https://developers.openai.com/api/docs/guides/tools-tool-search), [compaction](https://developers.openai.com/api/docs/guides/compaction), and assistant-item `phase` handling.
`previous_response_id` preserves prior assistant state automatically.
For stateless or Zero Data Retention flows, pass back the relevant returned output items on each turn.
See [Passing context from the previous response](https://developers.openai.com/api/docs/guides/conversation-state#passing-context-from-the-previous-response).

### Phase Parameter

When manually replaying assistant output items, preserve each original `phase` value unchanged.
This matters most for reasoning, preambles, repeated tool calls, and final answers after intermediate updates.
Use `phase: "commentary"` for intermediate user-visible updates and `phase: "final_answer"` for the completed answer.
Do not add `phase` to user messages.
See [Phase parameter](https://developers.openai.com/api/docs/guides/reasoning#phase-parameter).
