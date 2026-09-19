---
name: typesafe-ai
license: MIT
description: >
  Build AI-powered software with TypeSafe: small units of AI intelligence you
  can use like programming primitives. Its System One models, including Jev,
  turn natural language and application state into typed judgments and
  probabilities that code can combine. Use when a feature needs programmable
  common sense, when brainstorming what AI could make possible in an app, or
  when an LLM prompt-and-parse step could become a structured decision.
  Applications include routing, ranking, extraction, verification, and
  interactive experiences; these are starting points, not the limits.
  Read the bundled docs and cookbooks to find useful patterns and discover new combinations.
---

# Build with TypeSafe

TypeSafe makes units of AI intelligence usable like programming primitives: small
judgments you can compose into larger capabilities. Its **System One models** return
fast, focused judgments that software can consume directly. **Jev** is TypeSafe's
flagship and first System One model. It understands natural language and returns
typed answers and probabilities rather
than generating text or reasoning explanations. Code owns the workflow; the model
supplies programmable common sense where ordinary code needs semantic understanding.

## Read the bundled docs

**The bundled TypeSafe docs are local snapshots for task use.**
The live TypeSafe docs remain the source of truth when freshness matters.
This skill gives direction; the docs carry concepts, prompting guidance, API contracts, SDK usage, models, limits, and worked examples.

- Start with the [reference index](references/index.md) and load only the relevant local file.
- The bundled references condense upstream pages into plain Markdown and remove site-specific components, duplicated boilerplate, and long demonstration output.
  The index records the upstream source for each local reference.
- Before writing an integration, read the API or chosen SDK reference and the question guidance relevant to the design.
  For a new workflow, also inspect the closest cookbook because it often shows a better decomposition than a generic classifier.
- If a bundled summary appears stale or omits a needed detail, consult the upstream source listed in the index or the installed SDK types.
  State any access limitation and avoid inventing version-dependent details.

| Task | Start here; follow the relevant details |
| --- | --- |
| Understand the programming model | [System One and workflow concepts](references/concepts.md) |
| Explore what to build | [Use-case shapes](references/concepts.md#where-it-fits), then a relevant cookbook from the index |
| Prepare inputs and questions | [State](references/concepts.md#state) and [question design](references/question-design.md) |
| Decide how to handle uncertainty | [Confidence and action policy](references/concepts.md#confidence-and-action-policy) |
| Write API code | [HTTP API](references/api/http.md), [Python SDK](references/sdk/python.md), or [JavaScript SDK](references/sdk/javascript.md) |
| Update an older integration | [v1 migration](references/api/migration-v1.md) and the installed SDK's current reference |

## Find the useful shape

Start from the behavior the user wants: what will the application show, select,
change, or hand off? Work backward to the judgments it needs. Keep known rules,
calculations, exact lookups, and execution in code. Preserve the user's chosen stack
and scope; add TypeSafe where semantic understanding helps.

When brainstorming or choosing an architecture, consider more than classification.
The patterns below are starting points: combine primitives around the user's goal,
including ideas that do not fit an established recipe.

- **Route and fill known arguments.** A request can select a handler and its typed
  parameters. Ask useful branch-specific questions up front and consume only the
  relevant answers. Explore [function calling](references/cookbooks/routing-and-extraction.md#function-calling)
  and [speculative fan-out](references/composition-patterns.md#speculative-fan-out).
- **Select instead of generate.** Find candidate values or source spans in code,
  use a judgment to select the intended one, then copy or normalize it. Code can
  also assemble source text into a formatted document or reading guide. Explore
  [value extraction](references/cookbooks/routing-and-extraction.md#pre-parsed-value-extraction)
  and [structure recovery](references/cookbooks/routing-and-extraction.md#structure-recovery).
- **Find and judge evidence.** Retrieve candidates, compare their relevance to a
  query, and select useful context. Explore [reranking](references/cookbooks/retrieval-and-classification.md#reranking)
  and [hierarchical classification](references/cookbooks/retrieval-and-classification.md#hierarchical-classification).
- **Turn judgments into reusable data.** Score dimensions once, then let code or
  user controls change weights, thresholds, rankings, and views. With labeled
  outcomes, those signals can become classical ML features. Explore
  [composite scoring](references/composition-patterns.md#composite-scoring) and
  [feature discovery](references/cookbooks/verification-and-learning.md#feature-discovery).
- **Verify and escalate.** Check specific claims or fields against their evidence;
  send uncertain or failing cases to a person or reasoning model. Explore
  [citation checks](references/cookbooks/verification-and-learning.md#citation-verification) and
  [extraction cascades](references/cookbooks/verification-and-learning.md#structured-data-extraction-cascade).
- **Respond to changing state.** Code can retain goals and observations while fresh
  judgments guide the next bounded step. Keep inferred state distinct from observed
  facts, and check freshness before applying a result to a changed situation.

For open-ended requests, offer the few directions that best serve the user's goal
and recommend a starting point. For a concrete request, choose the relevant pattern
and build; a brainstorm is not a mandatory detour.

## Design the judgments

Choose by what the answer means, then read the relevant primitive page:

| Need | Primitive | Important distinction |
| --- | --- | --- |
| One of a defined set | [Choice](references/question-design.md#choice) | Picks one option; its distribution compares competing options |
| Whether a condition holds | [Noul](references/question-design.md#noul) | Probability of yes; no separate confidence; use one per label when several may apply |
| Degree along a described dimension | [Score](references/question-design.md#score) | Probability-weighted position on ordered levels; use comparable per-item Scores for graded ranking |

Give each question enough relevant **state** to answer: source text, identities,
relationships, policies, and current facts. Prefer named JSON fields when context
has several parts. Put the judgment in **instructions** and define its possible
answers in **criteria**. Question IDs are for code and are not sent to the model;
include complete meaning in the question. Reference nested state with backticked
paths such as `ticket.messages[0].text`.

Ask one narrow, coherent judgment per question. Split independently useful dimensions,
without destroying the relationship being judged. A bounded action selection or
contextual interpretation is valid; atomic does not mean literal fact extraction
or a one-sentence limit. Strings work for simple questions. Use structured objects
or arrays when definitions, contrasts, exclusions, or examples clarify instructions
or criteria. Score levels must describe concrete situations and stand on their own.

Keep the needed answers available. Include a no-match outcome when nothing may fit;
use a separate presence judgment when it is independently useful. For source-value
selection, check candidate coverage: the model cannot choose an omitted value.

## Compose and verify

**Ask independent questions over the same state together**, including useful
speculative questions. They run in parallel and cannot see one another's answers.
State each speculative premise explicitly; code consumes the applicable answers.
A second request is warranted when an earlier answer is needed to fetch evidence,
construct new state, or determine the next options. Extra questions still use tokens;
measure actual request budgets, cost, and end-to-end latency.

Use probabilities and confidence to guide behavior, with thresholds evaluated on
the user's data and consequences. Choice/Score confidence summarizes distribution
concentration, not overall workflow correctness or permission to act. A Noul near
0.5 means similar probability for yes and no, not medium intensity. Several
acceptable alternatives can also spread probability; low confidence need not
invalidate a harmless preference choice. Ignore uncertainty on unused branches.

Keep policy explicit and raw judgments reusable. Weighted scores suit compensating
preferences; an “any serious violation” rule needs separate conditions. Changing a
weight or display filter need not rerun inference when evidence and question meanings
are unchanged. Typed output guarantees the interface, not truth. System One models
are trained for calibrated decisions; validate their performance in the target domain.

Test representative cases and the resulting application behavior. For failures,
inspect the exact state, questions, candidates, answers, composition, and observed
outcome. Separate missing evidence, model errors, code errors, and service failures.
Treat cookbook thresholds and demo results as examples to evaluate, not universal
rules or permanent model limitations. Keep API credentials server-side in web apps.
