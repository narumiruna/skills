# Using GPT-6

Source: adapted from the [official GPT-6 guide](https://developers.openai.com/api/docs/guides/latest-model), including its [prompting best practices](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices) and [migration guidance](https://developers.openai.com/api/docs/guides/latest-model#migration-quickstart).

## Models and Reasoning Effort

This reference covers the exact model IDs below, including GPT-6.1 Sol and Terra.
It does not establish other aliases or cover later models by name alone.

| Model ID | Main use | Supported reasoning effort |
| --- | --- | --- |
| [`gpt-6-astra`](https://developers.openai.com/api/docs/models/gpt-6-astra) | Demanding reasoning, coding, computer use, and professional work | `low`, `medium`, `high`, `xhigh`, `max` |
| [`gpt-6.1-sol`](https://developers.openai.com/api/docs/models/gpt-6.1-sol) | Complex coding, computer use, and professional work at a lower cost than Astra | `low`, `medium`, `high`, `xhigh`, `max` |
| [`gpt-6.1-terra`](https://developers.openai.com/api/docs/models/gpt-6.1-terra) | Visual reasoning, precise computer use, and writing | `none`, `low`, `medium`, `high`, `xhigh`, `max` |
| [`gpt-6-luna`](https://developers.openai.com/api/docs/models/gpt-6-luna) | Focused, high-volume tasks | `none`, `low`, `medium`, `high`, `xhigh`, `max` |
| [`gpt-6-sol`](https://developers.openai.com/api/docs/models/gpt-6-sol) | Earlier Sol model for coding and agent workflows | `none`, `low`, `medium`, `high`, `xhigh`, `max` |

- Preserve the current effective reasoning effort during migration when the target model supports it.
- GPT-6 Astra and GPT-6.1 Sol do not support `none`; start with `low` instead.
- If an existing request uses `minimal`, start with `low` and compare representative tasks.
- GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna, and GPT-6 Sol default to `medium`.
- Use `reasoning.effort` in Responses or `reasoning_effort` in Chat Completions.

## Model-Specific Behavior

The [official prompting notes](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices) report these behaviors for GPT-6 Astra, not measured results for every GPT-6 model:

- More clarification and approval pauses than earlier models, including when the user expects continued work.
- Greater sensitivity to unclear or conflicting instructions in skills and `AGENTS.md` files.
- Detailed, formatted responses with recurring phrases.
- Less subagent delegation than some workflows need.
- Broader or more repeated verification than small changes require.

## API Compatibility

### Endpoints and Parameters

Use the [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses) for reasoning with tools and multi-turn workflows.

- GPT-6 Astra, GPT-6.1 Sol, and GPT-6.1 Terra support Chat Completions, but tool calling requires Responses, including when Terra uses `none`.
- GPT-6 Sol and GPT-6 Luna support function calling in Chat Completions only with `reasoning_effort: "none"`.
- When reasoning effort is not `none`:
  - Remove `temperature`, `top_p`, and `top_logprobs`.
  - For Chat Completions, also remove `logprobs`.
  - For Responses, remove `message.output_text.logprobs` from `include`.

### Tools and Conversation State

- **Async tool calling:** Set `async: true` on a function or custom tool to let GPT-6 continue independent work while the application runs it.
  The application still executes the tool and returns its result with the original `call_id`.
  See [Async tool calling](https://developers.openai.com/api/docs/guides/async-tool-calling).
- **Mid-turn steering:** Over a WebSocket connection, the Responses API can preserve completed work and include new user instructions in a continuation.
  See [Mid-turn steering](https://developers.openai.com/api/docs/guides/steering) for events and tool-result handling.
- **Reasoning changes:** Use `configuration_update` input items to change effort between responses in supported standard, single-agent requests.
  Keep request-level `reasoning.effort` unchanged to preserve the prompt prefix for caching.
  The new effort applies until another update overrides it.
  Check [compatibility limits](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) before use.
- **Programmatic Tool Calling:** The GPT-6 guide lists support for [Programmatic Tool Calling](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling).
  Check its tool eligibility and continuation requirements before use.
- **Other family capabilities:** The guide also lists [multi-agent orchestration](https://developers.openai.com/api/docs/guides/responses-multi-agent), [persisted reasoning](https://developers.openai.com/api/docs/guides/reasoning#preserve-reasoning-across-calls), [compaction](https://developers.openai.com/api/docs/guides/compaction), and [pro mode](https://developers.openai.com/api/docs/guides/reasoning#reasoning-mode).
  Check each feature's compatibility requirements instead of inferring them from the model name.

### Processing and Data Residency

- Fast mode supports EU data residency for GPT-6.1 Sol, GPT-6.1 Terra, and GPT-6 Luna, but not GPT-6 Astra or GPT-6 Sol.
- GPT-6.1 Sol Ultrafast supports US and EU data residency and global processing.
- GPT-6 Astra Ultrafast supports US data residency and global processing only.
- GPT-6 Astra Fast mode does not include a latency SLA.

See [Fast mode compatibility](https://developers.openai.com/api/docs/guides/fast-mode#is-fast-mode-compatible-with-data-residency-zero-data-retention-and-a-baa), [Ultrafast mode](https://developers.openai.com/api/docs/guides/ultrafast-mode), and [data residency eligibility](https://developers.openai.com/api/docs/guides/your-data#which-models-and-features-are-eligible-for-data-residency) before choosing a processing mode.

## Migration Checks

- When moving from GPT-6 Sol to GPT-6.1 Sol, account for the loss of `none` reasoning effort and Chat Completions function calling.
- When moving from GPT-5.6 Terra to GPT-6.1 Terra, compare representative images and workflows at the same reasoning effort.
  Move Chat Completions tool calls to Responses.
- When moving from GPT-5.5 or earlier, replace `prompt_cache_retention` with `prompt_cache_options.ttl` set to `"30m"`.
  Review [prompt caching changes](https://developers.openai.com/api/docs/guides/prompt-caching#summary-of-model-differences), including cache boundaries and cache-write billing.
