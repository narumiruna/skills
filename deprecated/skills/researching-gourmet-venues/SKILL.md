---
name: researching-gourmet-venues
description: Deprecated internal workflow for auditable city-based food research with multi-source evidence, scope-checked rankings, standardized scoring, and synchronized candidate, recommendation, and exclusion files.
metadata:
  internal: true
---

# Researching Gourmet Venues (Deprecated Reference)

This rarely used workflow is excluded from active discovery but retained for explicit local compatibility. Keep evidence, scores, and decisions traceable across a six-file city research pack.

## Initialize

1. Resolve city and output language. Ask once only when language is unspecified, then record it in `overview.md`.
2. Copy `assets/templates/` into `gourmet/<city-slug>/` to create `overview.md`, `inbox.md`, `candidates.md`, `notes.md`, `top-places.md`, and `excluded.md`; replace placeholders before research.
3. Preserve original-language venue names unless the user requests translation.

Never fabricate sources, ratings, hours, or claims. Use `unknown`. Never delete a candidate: mark it `rejected` and record the reason in `excluded.md`.

## Research and Score

1. Capture raw discoveries in `inbox.md`, then move viable entries to `candidates.md` with status.
2. Build a `notes.md` evidence block for each candidate with practical constraints. Require four independent source roles by default: official channel, maps/aggregator, local reviews, and guide/editorial.
3. In an information-sparse locale, use three sources only after recording `evidence: limited`, why, and attempted sources. Do not score or publish a recommendation with fewer sources outside this exception.
4. When repeated service complaints, hygiene/safety concerns, tourist-trap claims, extreme queues, inconsistent ratings, or unclear access appear, add a focused negative-review section and reflect it in scoring.
5. Score and justify each component: Taste/Quality, Value, Convenience, Consistency, and Risk (0–10 each; higher Risk score means lower practical risk).
6. Classify totals: Top Pick ≥35, Backup 30–34, Reject <30 or a hard safety/tourist-trap exclusion.
7. Synchronize status and score across `notes.md`, `candidates.md`, `top-places.md`, and `excluded.md`. Leave no unresolved `inbox` status in the final pack.

## Ranking Retrieval

Before returning “highest score” or top-N results, confirm:

- exact geographic boundary, including suburbs, islands, or neighboring regions
- overall versus cuisine/category scope
- source URL/page title and any area identifier

Handle consent, language, or location gates so list items actually render. If static extraction fails, use available browser tooling; do not substitute a nearby ranking scope. Record exclusions needed to enforce the requested boundary.

## Verification

Check all six files exist; language and original-name policy are recorded; claims and ratings have sources or `unknown`; limited evidence and negative-review triggers are documented; score arithmetic and thresholds are correct; and every candidate appears consistently in recommendation or exclusion outputs.

Return the requested recommendations first, then source coverage, score rationale, practical caveats, and any unresolved evidence gap.
