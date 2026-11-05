---
latestModelInfo:
  model: gpt-6-astra
  migrationGuide: /api/docs/guides/latest-model/gpt-6-astra.md#migration-quickstart
  promptingGuide: /api/docs/guides/latest-model/gpt-6-astra.md#prompting-best-practices
---

# Using GPT-6 Astra

Source: condensed from [OpenAI documentation](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra), as supplied by the user.

Use the [GPT-6 family reference](gpt-6.md) for current model coverage, behavior notes, and API features.

## API and Migration Notes

Set `model` to `gpt-6-astra`, then check the following:

- **Reasoning effort:** If you currently use `none` or `minimal`, start with `low` and compare results.
  Otherwise, preserve your current effective [reasoning effort](https://developers.openai.com/api/docs/guides/reasoning#reasoning-effort).
  Use `reasoning.effort` in Responses or `reasoning_effort` in Chat Completions.
- **Tool calling:** Use the [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses#migrating-from-chat-completions).
  GPT-6 Astra supports Chat Completions, but tool calling requires Responses.
- **Unsupported parameters:** Remove `temperature`, `top_p`, and `top_logprobs`.
  For Chat Completions, also remove `logprobs`.
  For Responses, remove `message.output_text.logprobs` from `include`.
- **Fast mode:** For EU data residency, use Standard processing.
  GPT-6 Astra does not support `service_tier: "fast"` or `service_tier: "priority"` with EU data residency.
  Fast mode for GPT-6 Astra does not include a latency SLA.
  See [Fast mode compatibility](https://developers.openai.com/api/docs/guides/fast-mode#is-fast-mode-compatible-with-data-residency-zero-data-retention-and-a-baa).
- **Changing reasoning effort:** If your application changes effort between responses, use `configuration_update` items in standard, single-agent requests.
  Keep request-level `reasoning.effort` unchanged to preserve the prompt prefix for caching.
  Check the [compatibility limits](https://developers.openai.com/api/docs/guides/reasoning#change-reasoning-mid-conversation) before adopting this feature.
- **Prompt caching:** When migrating from GPT-5.5 or earlier, replace `prompt_cache_retention` with `prompt_cache_options.ttl` set to `"30m"`.
  Review the [prompt caching changes](https://developers.openai.com/api/docs/guides/prompt-caching#summary-of-model-differences), including cache boundaries and cache-write billing.
- **Misalignment monitoring:** Astra's safeguards asynchronously monitor for misalignment and trigger alerts.
  See [Misalignment monitoring](https://developers.openai.com/api/docs/guides/safety-checks/misalignment-monitoring).
