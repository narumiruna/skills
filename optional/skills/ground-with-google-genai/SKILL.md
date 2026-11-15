---
name: ground-with-google-genai
description: Run one-shot Google Gemini research through the official Google GenAI Interactions API with Google Search, Google Maps, or URL Context grounding and inspect citation evidence. Use when Codex needs current web grounding, place or local recommendations, answers about specific public HTTP(S) URLs, or an explicit Gemini/Google GenAI grounded response.
---

# Grounding With Google GenAI

Use the bundled `scripts/google_genai_grounding.py` by absolute path. Default to `gemini-3.5-flash`; pass `--model` only when the user requests another compatible model. The script sends stateless requests with `store=false` and emits JSON containing the answer, citations, bounded tool evidence, and usage.

## Select Grounding

- Use `search` for current or open-web facts that benefit from Google Search citations.
- Use `maps` for places, local recommendations, addresses, reviews, or proximity. Supply both coordinates when the user's relevant location is known; omit both otherwise. Google Maps grounding currently requires English prompts and responses, so query in English and translate the cited answer afterward when needed.
- Use `url` to read or compare one to 20 specific public `http://` or `https://` pages. Prefer direct content URLs. Do not use it for localhost, private networks, login-only or paywalled pages, Google Workspace files, YouTube, or audio/video URLs.

## Run One Request

Resolve `SKILL_DIR` to this skill directory and require `GEMINI_API_KEY` in the process environment or a discoverable `.env` file. The script loads `.env` with `python-dotenv` without overriding an existing environment value. Never print, log, place in arguments, or write the key to repository files.

Run Google Search grounding:

```shell
uv run --script "$SKILL_DIR/scripts/google_genai_grounding.py" search \
  'What changed in the current release? Cite primary sources.'
```

Run Google Maps grounding, adding coordinates only when relevant:

```shell
uv run --script "$SKILL_DIR/scripts/google_genai_grounding.py" maps \
  'Find a well-reviewed coffee shop within a 15-minute walk.' \
  --latitude 25.033 --longitude 121.5654
```

Run URL Context with one `--url` per source:

```shell
uv run --script "$SKILL_DIR/scripts/google_genai_grounding.py" url \
  'Compare the documented behavior and identify material differences.' \
  --url 'https://example.com/one' \
  --url 'https://example.com/two'
```

An explicit request to use Gemini, Google GenAI, or this skill authorizes one bounded grounding call. If this skill was selected implicitly because web, place, or URL grounding would help, confirm before consuming Google API quota. Retry once only for a clear transient failure or a corrected deterministic input, and do not fan out into extra calls without need.

## Verify and Answer

Inspect `citations`, `tool_steps`, and `usage` before relying on `text`:

- Require a matching call/result step and relevant `url_citation` or `place_citation` evidence for grounded claims.
- For URL Context, require each needed URL retrieval to report `status: success`. Treat `error` or `unsafe` as failed retrieval even if the model produced plausible text.
- If grounding was not used, a required source failed, or citations are absent, disclose that the answer was not verified; do not present model text as grounded evidence.
- Preserve citation names and links in the final answer. Attribute Maps-derived claims to Google Maps and keep place links intact.
- Report the selected model and any unavailable check when it matters. An empty `interaction_id` is expected for stateless requests.

Stop after the grounded answer and its material caveats are complete. Do not broaden a specific URL request into general web research unless the user asks for both.
