---
latestModelInfo:
  model: gpt-5.6-sol
  migrationGuide: /api/docs/guides/upgrading-to-gpt-5p6-sol.md
  promptingGuide: /api/docs/guides/prompt-guidance-gpt-5p6.md
---

# Using GPT-5.6

Source: condensed from the [official GPT-5.6 guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6).

## Models and Behavior Changes

- This reference covers `gpt-5.6-sol`, `gpt-5.6-terra`, and `gpt-5.6-luna`.
  The `gpt-5.6` alias routes to `gpt-5.6-sol`.
- GPT-5.6 is more concise by default than GPT-5.5; inherited brevity instructions can make answers too short.
- Repeated approval rules can cause unnecessary pauses for routine local actions.

## API and Migration Notes

- GPT-5.6 supports `none`, `low`, `medium`, `high`, `xhigh`, and `max` reasoning effort.
  The default is `medium` in standard and pro modes.
  When migrating from GPT-5.5 or GPT-5.4, compare the current setting and one level lower.
- Use the [Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses) for reasoning, tool-calling, and multi-turn workflows.
- Enable [pro mode](https://developers.openai.com/api/docs/guides/reasoning#reasoning-mode) with `reasoning.mode: "pro"`, not a separate model slug.
  Mode and effort are independent settings.
  Reported usage aggregates the additional model work, billed at the selected model's standard token rates.
- [Multi-agent orchestration](https://developers.openai.com/api/docs/guides/responses-multi-agent) is a beta feature in Responses.
- `original` and `auto` image detail preserve image dimensions subject to the [image input limits](https://developers.openai.com/api/docs/guides/images-vision#image-input-requirements), which can increase input tokens and latency.
- `text.verbosity` supports `low`, `medium`, and `high`.
  See [verbosity configuration](https://developers.openai.com/api/docs/guides/deployment-checklist#set-up-textverbosity).

### Persisted Reasoning

- Omit `reasoning.context` or use `auto` to select the model default; check the response's `reasoning.context` for the effective mode.
- Use `all_turns` to retain earlier reasoning and continue with `previous_response_id`.
  With manual history, preserve prior user inputs and every response output item.
  For `store: false` or Zero Data Retention, replay the encrypted reasoning items returned by the API.
- Use `current_turn` when earlier reasoning is no longer relevant.

See [persisted reasoning](https://developers.openai.com/api/docs/guides/reasoning#preserve-reasoning-across-calls).

### Prompt Caching

- Implicit caching remains available without code changes.
- Cache writes cost 1.25× the uncached input rate; inspect `cached_tokens` and `cache_write_tokens` for net cost.
- Explicit breakpoints or `prompt_cache_options.mode: "explicit"` control cache writes.
- Replace `prompt_cache_retention` with `prompt_cache_options.ttl`.

See [prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching).

## Programmatic Tool Calling

- Add `programmatic_tool_calling` and opt eligible tools in with `allowed_callers`.
- Handle `program` items, program-issued function calls, and `program_output` items while preserving each call's `call_id` and `caller` linkage.
- `program_output` and the final assistant `message` are separate outputs.
- Programmatic Tool Calling is Zero Data Retention-compatible and has no additional container costs.

See the [Programmatic Tool Calling guide](https://developers.openai.com/api/docs/guides/tools-programmatic-tool-calling) for tool eligibility and continuation requirements.

## Generation Safeguards

Cyber and biology misuse classifiers can block requests or pause generation mid-stream, including on legitimate dual-use work.
For individual end-user applications, send a stable, privacy-preserving [`safety_identifier`](https://developers.openai.com/api/docs/guides/safety-best-practices#implement-safety-identifiers).
