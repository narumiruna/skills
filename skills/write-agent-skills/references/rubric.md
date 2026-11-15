# Agent Skill Scoring Rubric

Assign an integer score from 1 to 10 for every assessable dimension. Use these shared anchors:

| Score | Meaning |
| --- | --- |
| 10 | Exemplary: no material weakness found in the inspected scope |
| 9 | Excellent: only minor, non-material improvement remains |
| 8 | Strong: reliable with one or more localized limitations |
| 7 | Adequate: usable, but notable improvement is warranted |
| 6 | Workable: a material gap limits reliability or completeness |
| 5 | Inconsistent: useful elements exist, but substantial correction is needed |
| 4 | Weak: defects regularly interfere with correct application |
| 3 | Severe: only a small portion of the dimension is reliable |
| 2 | Effectively absent or materially misleading |
| 1 | Actively harmful or incompatible with the intended task |

Use the full range when evidence supports it. Intermediate differences must reflect inspected evidence rather than a preference for round numbers.

## Trigger clarity

Assess whether frontmatter states both what the skill does and when it should activate. Check specificity, collision risk with sibling skills, explicit-invocation requirements where needed, and alignment among name, description, and catalog text.

Lower the score for vague domain labels, trigger rules hidden only in the body, materially overlapping descriptions without routing, or mismatched discovery surfaces.

## Workflow actionability

Assess whether the post-trigger body lets another agent complete the task. Look for clear outcomes, relevant context gathering, executable decisions, justified sequencing, scope control, stopping conditions, and a defined deliverable.

Lower the score for generic advice, over-prescribed routine steps, missing decisions, plans that cannot be executed, or workflows that stop before the requested outcome.

## Safety boundaries

Assess authorization and risk controls proportionately to the skill's actual effects. Local read-only work may need only a concise boundary; external writes, destructive actions, credentials, costs, publication, and remote mutations require explicit approval and verification rules.

Lower the score for overbroad authority, missing target/content approval, secret exposure, unsafe recovery, or blanket confirmation gates that unnecessarily block safe local work.

## Verification rigor

Assess whether important claims and outcomes require direct, relevant evidence. Look for focused checks, representative validation, current-snapshot verification, honest handling of unavailable checks, and separation between source inspection, structural validation, rendering, runtime behavior, and external state.

Apply this proportionately: an explanatory skill need not require a test suite, but it should ground claims in available sources and distinguish evidence from inference. Lower the score for unverified completion claims, stale evidence, vague “test it” language, or checks that cannot prove the stated outcome.

## Incremental knowledge value

Assess how much task-relevant guidance the skill adds beyond the declared target-model baseline. Reward non-obvious decision rules and trade-offs, real-world failure modes, current version or repository constraints, critical ordering, and concise reminders with evidence or a concrete failure rationale.

Label representative passages rather than every paragraph:

- **Domain delta:** specialized facts, decisions, constraints, or failure handling that materially extends the baseline.
- **Justified activation:** likely familiar knowledge whose brief reminder has evidence or a concrete failure rationale for improving reliable application.
- **Redundancy candidate:** generic background, basic tutorials, routine operations, repeated rules, or decorative examples with no identified behavioral value.

Use these dimension-specific landmarks together with the shared anchors; use intermediate scores when the evidence falls between them:

| Score | Incremental-value landmark |
| --- | --- |
| 10 | Substantive guidance is concentrated domain delta or justified activation, with no material redundancy found. |
| 8 | Strong task-specific value with only localized baseline restatement. |
| 6 | Useful specialized guidance is materially diluted by generic or routine content. |
| 4 | The body is mostly baseline explanation or tutorial content with little non-obvious guidance. |
| 2 | It provides effectively no task-relevant increment or materially mischaracterizes baseline knowledge. |

Do not mark concise disambiguation, current facts, safety or authorization boundaries, output contracts, stopping conditions, or evidence-backed error prevention as redundant solely because the model may know them. Static inspection supports only an inferred increment; representative baseline-versus-skill evaluations can establish an observed gain.

## Leanness and maintainability

Assess whether every instruction earns its context cost. Look for one clear purpose, low repetition, outcome-focused constraints, direct on-demand resource routing, aligned metadata, bounded examples, and stable guidance rather than incidental implementation detail.

Lower the score for duplicated trigger sections, generic background, decorative examples, unjustified files, repeated approval language, oversized unstructured bodies, or version-sensitive facts without a verification path. Do not penalize necessary complexity merely because a high-risk workflow is longer.

Judge organization and context economy separately from novelty: a concise generic skill can be lean but low in incremental value, while a necessarily detailed fragile workflow can score well in both.

## Overall score

Use equal weighting across assessed dimensions. With complete evidence:

```text
overall = (trigger + workflow + safety + verification + incremental value + leanness) / 6
```

When review-environment limitations make a dimension materially unassessable, do not convert that uncertainty into a low score. Mark the dimension `unassessed`, exclude it from the aggregate, and calculate a provisional overall from the assessed dimensions:

```text
provisional overall = sum(assessed dimension scores) / count(assessed dimensions)
```

Report coverage such as `5/6 dimensions`, the unavailable evidence, and confidence. Do not rank or directly compare aggregate scores with different coverage, or compare this six-dimension aggregate directly with historical five-dimension scores. Display a full or provisional result to one decimal place; do not round or normalize individual scores, apply a curve, or convert repository test results into bonus points.
