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

## Prompting Best Practices

The official guide provides shared GPT-6 prompting examples based on behavior observed with GPT-6 Astra.
Use them as a starting point and evaluate them with the selected model and workload.
Do not present Astra behavior notes as measured behavior for every GPT-6 model.

### Initiative and Follow-through

Astra can ask for clarification or stop for review where earlier models would continue.
Define the intended result, authorized actions, and completion conditions so the model can finish the task.
For action requests, make clear that a plan or first implementation is not the completion point unless the workflow requires it.

Adapt the guide's autonomy examples to the application's approval boundaries:

```text
For change requests, complete the authorized, in-scope work and required checks.
Do not stop after a plan or partial implementation when the request requires a finished result.
Before asking for approval, finish the authorized preparation needed to make the proposed action concrete and reviewable.
Ask before external writes, destructive or costly actions, or a material expansion of scope unless that exact action is already authorized.
Ask a focused question when missing information materially changes the result; otherwise, continue with reasonable assumptions.
```

### Instruction Following

Astra can be sensitive to unclear or conflicting instructions in skills and `AGENTS.md` files.
Audit those instructions when they cause unnecessary pauses or change the intended task.
Make instruction priority explicit according to the host's instruction hierarchy.
Skill guidance must not silently replace the user's explicit task or override higher-priority requirements.

When a skill causes the model to ask for approval, stop early, or change direction, require it to identify and link the exact file, quote the relevant instruction, and explain how it applies.
Distinguish an explicit requirement from the model's interpretation.

### Personality and Writing Style

Astra can produce detailed, formatted responses and recurring phrases.
Specify observable writing choices that match the audience and product:

- State the main point early, then give the necessary explanation and evidence.
- Use familiar words, precise verbs, active voice, and one main idea per paragraph.
- Use lists when the items are parallel, sequential, or easier to compare.
- Include technical detail to the extent that it helps the reader understand the result.
- Remove stock phrases, invented labels, and unsolicited contrasts or summaries.

### Subagent Delegation

Astra may delegate less often than the application needs.
Specify when independent work should run in parallel and how much delegation the workflow permits.
Use delegation when it can reduce elapsed time or improve quality, rather than on every task.
Define who combines and checks the results.
Keep messages between agents legible, with proper spacing between words and numbers.

### Testing and Verification

Astra can perform broader or more repeated checks than a small change requires.
Set the required verification scope and completion point:

```text
Run checks appropriate to the change and complete all required validation.
Do not add tests for reversible, low-impact changes that only repeat the implementation.
After required checks pass, broaden or repeat verification only for new changes, failures, or unresolved concerns.
```

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
- Evaluate prompt changes on the selected model before adoption.
  Compare task success, answer completeness, required evidence, total tokens, latency, and cost.
  Treat fewer calls or tokens as an improvement only when the result still meets the required quality level.
