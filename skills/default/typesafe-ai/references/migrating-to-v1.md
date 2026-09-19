> ## Documentation Index
> Fetch the complete documentation index at: https://docs.typesafe.ai/llms.txt
> Use this file to discover all available pages before exploring further.

# Migrating to the v1 API

> Move from the preview evaluation endpoint to the stable v1 API.

The preview endpoint (`/preview/evaluation`) is replaced by the stable **v1** endpoint (`/v1/systemone`). This is a **breaking change**: the endpoint, the request shape, and the response shape all changed. This page lists each delta with a before/after example so you can update your integration.

Auth is unchanged — keep sending `Authorization: Bearer <API_KEY>` and `Content-Type: application/json`.

## At a glance

| Area                                                            | Preview                                   | v1                                           |
| --------------------------------------------------------------- | ----------------------------------------- | -------------------------------------------- |
| [Endpoint](#1-endpoint-rename)                                  | `POST /preview/evaluation`                | `POST /v1/systemone`                         |
| [Questions](#2-prompts-array-becomes-a-questions-map)           | `prompts` array (each carries a `key`)    | `questions` map (the key is the id)          |
| [Descriptors](#3-unified-criteria-per-question-type)            | per-type: `criteria`, `options`, `levels` | unified `criteria` per type                  |
| [Answers](#4-responses-array-becomes-an-answers-map)            | `responses` array (same order)            | `answers` map (keyed by your id)             |
| [noul value](#5-renamed-answer-value-fields)                    | `probability`                             | `noul`                                       |
| [choice value](#5-renamed-answer-value-fields)                  | `chosen`                                  | `choice`                                     |
| [score value](#5-renamed-answer-value-fields)                   | `expectation`                             | `score`                                      |
| [choice `probabilities`](#6-choice-probabilities-becomes-a-map) | array of `{ option, probability }`        | map of `option → probability`                |
| [score `probabilities`](#6-choice-probabilities-becomes-a-map)  | — (not returned)                          | map over levels (new in v1)                  |
| [Confidence](#7-confidence-is-a-new-computation)                | old computation                           | new computation                              |
| [Usage](#8-usage-reports-token-counts)                          | `usage.billing_units` placeholder         | `usage.input_tokens` / `usage.output_tokens` |
| [Input field](#9-document-becomes-state)                        | `document`                                | `state`                                      |
| [Python SDK](#python-sdk)                                       | `typesafe-client`                         | `typesafe-sdk` (new package)                 |

## 1. Endpoint rename

`evaluation` became `systemone`.

```diff theme={null}
- POST https://api.typesafe.ai/preview/evaluation
+ POST https://api.typesafe.ai/v1/systemone
```

## 2. `prompts` array becomes a `questions` map

In preview, you sent a `prompts` **array** where each item carried its own `key`, and answers came back in the same order. In v1, you send a `questions` **map**: the map key is an id of your choice, and answers come back mapped to the same id.

```jsonc theme={null}
// preview — POST /preview/evaluation
{
  "model": "jev-latest",
  "document": "Sample document",
  "prompts": [
    { "key": "test_noul", "type": "noul", "instructions": "Test instructions" }
  ]
}
```

```jsonc theme={null}
// v1 — POST /v1/systemone
{
  "model": "jev-latest",
  "state": "Sample document",
  "questions": {
    "test_noul": { "type": "noul", "instructions": "Test instructions" }
  }
}
```

## 3. Unified `criteria` per question type

Every question type now describes itself with a field named `criteria`. The shape of `criteria` differs by type:

* **Noul** — `criteria?: { true?, false? }`. An optional object describing the two outcomes. New feature in v1!
* **Choice** — `criteria: { <option>: description }`. A map of option labels to their descriptions; use `null` when an option needs no explanation. Was an `options` array of `{ option, description? }`.
* **Score** — `criteria: [description, ...]`. A bare array of level descriptions; the level is the 0-indexed array position. Was a `levels` array of explicit `{ level, description }` objects. You can no longer skip levels; it was an anti-pattern now addressed by design.

### Choice criteria

```jsonc theme={null}
// preview
{
  "key": "test_choice",
  "type": "choice",
  "instructions": "Test instructions",
  "options": [
    {
      option: "Option A",
      description: "Description A"
    },
    {
      option: "Option B",
      description: "Description B"
    }
  ]
}
```

```jsonc theme={null}
// v1 (within "questions")
"test_choice": {
  "type": "choice",
  "instructions": "Test instructions",
  "criteria": {
    "Option A": "Description A",
    "Option B": "Description B"
  }
}
```

### Score criteria

```jsonc theme={null}
// preview
{
  "key": "test_score",
  "type": "score",
  "instructions": "Test instructions",
  "levels": [
    { "level": 0, "description": "Poor" },
    { "level": 1, "description": "Good" },
    { "level": 2, "description": "Excellent" }
  ]
}
```

```jsonc theme={null}
// v1 (within "questions")
"test_score": {
  "type": "score",
  "instructions": "Test instructions",
  "criteria": ["Poor", "Good", "Excellent"]
}
```

## 4. `responses` array becomes an `answers` map

Preview returned a `responses` **array** in the same order as your prompts, with each item containing a `key` property. v1 returns an `answers` **map** keyed by the question id you chose.

```jsonc theme={null}
// preview
{
  "responses": [
    { "key": "test_noul", "type": "noul", "probability": 0.92 }
  ]
}
```

```jsonc theme={null}
// v1
{
  "answers": {
    "test_noul": { "type": "noul", "noul": 0.92 }
  }
}
```

## 5. Renamed answer value fields

The core value field on each answer type was renamed:

| Type   | Preview field | v1 field |
| ------ | ------------- | -------- |
| Noul   | `probability` | `noul`   |
| Choice | `chosen`      | `choice` |
| Score  | `expectation` | `score`  |

## 6. Choice `probabilities` becomes a map

A Choice answer's `probabilities` changed from an **array** of `{ option, probability }` objects to a **map** of `option → probability`. (Score answers now also include a `probabilities` map over their levels, which preview did not return at all.)

```jsonc theme={null}
// preview
"probabilities": [
  { "option": "billing", "probability": 0.08 },
  { "option": "technical", "probability": 0.85 }
]
```

```jsonc theme={null}
// v1
"probabilities": { "billing": 0.08, "technical": 0.85 }
```

## 7. Confidence is a new computation

The computation behind `confidence` changed to make the value reliable, so the value will differ from preview even for an identical evaluation. Any logic your integration uses based on confidence should be carefully re-evaluated.

v1 also returns the full probability distribution for both Choice and Score. Since `confidence` is a statistic over that distribution, you can compute your own measure from the response. If you would like to re-create the same value that preview called "confidence" use a normalized-entropy computation. Here it is in Python:

```python theme={null}
import math

def normalized_entropy_confidence(probabilities: dict[str, float]) -> float:
    """Reproduce preview's confidence: 1 − normalized Shannon entropy of the
    distribution. Returns 1.0 when all weight is on one outcome, 0.0 when the
    distribution is perfectly uniform."""
    ps = [p for p in probabilities.values() if p > 0]
    n = len(probabilities)
    if n <= 1:
        return 1.0
    entropy = -sum(p * math.log(p) for p in ps)
    return 1.0 - entropy / math.log(n)


# choice: probabilities maps each option -> probability
# score:  probabilities maps each level (string key) -> probability
answer = response.answers["department"]
my_confidence = normalized_entropy_confidence(answer.probabilities)
```

## 8. Usage reports token counts

Preview reported a placeholder `usage.billing_units`. v1 reports token counts instead: `usage.input_tokens` and `usage.output_tokens`.

```diff theme={null}
- "usage": { "billing_units": 1 }
+ "usage": { "input_tokens": 312, "output_tokens": 48 }
```

## 9. `document` becomes `state`

The field that carries the content to evaluate is named `state`. Preview, and the first v1 releases, called it `document`. v1 now accepts only `state`; a request with `document` fails validation.

```diff theme={null}
- "document": "Sample document",
+ "state": "Sample document",
```

The content itself is unchanged: a string, an object, or an array. See [State](/concepts/state).

## Full before/after example

### Request

```jsonc theme={null}
// preview — POST /preview/evaluation
{
  "model": "jev-latest",
  "document": "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP.",
  "prompts": [
    {
      "key": "is_urgent",
      "type": "noul",
      "instructions": "Does this message convey urgency?"
    },
    {
      "key": "department",
      "type": "choice",
      "instructions": "Which team should handle this?",
      "options": [
        { "option": "billing", "description": "Payment/invoicing" },
        { "option": "technical", "description": "Bugs/integrations" },
        { "option": "sales", "description": "Pricing/upgrades" }
      ]
    },
    {
      "key": "frustration",
      "type": "score",
      "instructions": "How frustrated is the customer?",
      "levels": [
        { "level": 0, "description": "Calm, stating facts" },
        { "level": 1, "description": "Frustrated but civil" },
        { "level": 2, "description": "Very angry" }
      ]
    }
  ]
}
```

```jsonc theme={null}
// v1 — POST /v1/systemone
{
  "model": "jev-latest",
  "state": "Hi, I've been trying to connect my Stripe account for 3 days and it keeps failing. I'm losing sales. Please help ASAP.",
  "questions": {
    "is_urgent": {
      "type": "noul",
      "instructions": "Does this message convey urgency?"
    },
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this?",
      "criteria": {
        "billing": "Payment/invoicing",
        "technical": "Bugs/integrations",
        "sales": "Pricing/upgrades"
      }
    },
    "frustration": {
      "type": "score",
      "instructions": "How frustrated is the customer?",
      "criteria": ["Calm, stating facts", "Frustrated but civil", "Very angry"]
    }
  }
}
```

### Response

```jsonc theme={null}
// preview response
{
  "model": "jev-latest",
  "responses": [
    { "key": "is_urgent", "type": "noul", "probability": 0.92 },
    {
      "key": "department",
      "type": "choice",
      "chosen": "technical",
      "probabilities": [
        { "option": "billing", "probability": 0.08 },
        { "option": "technical", "probability": 0.85 },
        { "option": "sales", "probability": 0.07 }
      ],
      "confidence": 0.82
    },
    {
      "key": "frustration",
      "type": "score",
      "expectation": 1.6,
      "confidence": 0.78
    }
  ],
  "usage": { "billing_units": 1 }
}
```

```jsonc theme={null}
// v1 response
{
  "model": "jev-latest",
  "answers": {
    "is_urgent": { "type": "noul", "noul": 0.92 },
    "department": {
      "type": "choice",
      "choice": "technical",
      "probabilities": { "billing": 0.08, "technical": 0.85, "sales": 0.07 },
      "confidence": 0.82
    },
    "frustration": {
      "type": "score",
      "score": 1.6,
      "legend": { "0": "Calm, stating facts", "1": "Frustrated but civil", "2": "Very angry" },
      "probabilities": { "0": 0.05, "1": 0.3, "2": 0.65 },
      "confidence": 0.78
    }
  },
  "usage": { "input_tokens": 312, "output_tokens": 48 }
}
```

## Python SDK

The v1 API is served by a new package, [`typesafe-sdk`](/sdk/python), installed from PyPI with `pip install typesafe-sdk`. The previous `typesafe-client` package (every release, `0.1.x` and `1.0.x`) sends `document` and no longer works against the API. All of the API changes above apply, plus these renames in the client:

| `typesafe-client`                                                      | `typesafe-sdk`                                                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `from typesafe_client import TypeSafeClient`                           | `from typesafe_sdk import TypeSafeClient` (and `AsyncTypeSafeClient`)                |
| `client.evaluate(...)` / `client.evaluate_async(...)`                  | `client.system_one(...)` / `await async_client.system_one(...)`                      |
| `*Prompt` dataclasses or `*Question` models                            | `Noul`, `Choice`, `Score` from `typesafe_sdk`                                        |
| `system_one(model, document, questions)`                               | `system_one(state, questions)`; `model` is optional and defaults to `jev-latest`     |
| Choice question `options`                                              | Choice question `criteria` (map of option → description)                             |
| Score question `levels`                                                | Score `criteria` (positional list of level descriptions)                             |
| `response[key]`, `response.noul(key)` / `.choice(key)` / `.score(key)` | `response.answers[key]`, or `response.nouls[key]` / `.choices[key]` / `.scores[key]` |
| Noul `.probability`                                                    | Noul `.noul`                                                                         |
| Choice `.chosen`                                                       | Choice `.choice`                                                                     |
| Score `.expectation`                                                   | Score `.score`                                                                       |

See the [Python SDK reference](/sdk/python) for installation, async usage, retries, and error handling.
