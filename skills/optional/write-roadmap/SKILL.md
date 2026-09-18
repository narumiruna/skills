---
name: write-roadmap
description: Create, revise, review, or track concise, outcome-oriented product and system roadmaps with phased milestone checkboxes and evidence-based progress, and delete them when complete; use write-plans for executable task planning and implementation tracking.
---

# Writing Roadmaps

A roadmap expresses strategic direction and sequencing, not a promise of delivery dates or an implementation checklist.
Creating or revising a roadmap authorizes changes to the roadmap artifact only, not implementation of its initiatives.
For a review-only request, report findings without rewriting unless asked.

## Ground the Roadmap

Inspect provided material and relevant repository evidence before drafting. Establish the audience, scope, planning horizon, and current baseline. Ask at most one question when a missing answer would materially change the roadmap; otherwise proceed with explicit assumptions or unknowns.

Separate verified current state, approved commitments, and proposed direction. Do not invent capabilities, dates, targets, owners, capacity, dependencies, or certainty.

Save a created or revised roadmap to the repository unless the user requests chat-only output.
Default to `docs/roadmaps/YYYY-MM-DD_<topic>-roadmap.md`; derive a concise lowercase kebab-case topic, create the directory when needed, and update that roadmap in place.

## Start with the Lean Template

Use this structure unless the user requests another format. Keep entries brief and expand only where evidence, rationale, or a decision needs explanation.

```markdown
# <Topic> Roadmap

## Vision

<Durable purpose and desired future state.>

## Objectives

- **<Outcome>** — Success: <grounded measure and horizon, or a material unknown/TBD.>

## Current State

- <Verified baseline, constraint, or challenge that explains the roadmap.>

## Roadmap

### Phase N: <outcome-focused name>

- [ ] <Observable delivered capability, validated assumption, or consequential decision.>

**Outcome:** <State this phase establishes and what it unlocks.>
```

Adapt the phase count and names to the evidence. Milestones must describe verifiable strategic results, not activities such as “work on,” “improve,” or “explore” without a decision criterion. Add dates or calendar ranges only when supplied or supported by evidence.

## Add Detail Only When Useful

Add only sections that materially improve a decision or explain the roadmap:

- **Guiding Principles** — Decision rules for real prioritization or tradeoff questions.
- **Roadmap Themes** — Strategic pillars connecting initiatives across phases; not team, component, or feature lists.
- **Success Metrics** — A fuller objective-linked view when baseline, target, horizon, or measurement source needs explanation.
- **Technical Health** — Cross-cutting stability, performance, security, scalability, maintainability, observability, or debt context; still place required work in the relevant phase.
- **Risks and Dependencies** — Material uncertainty, blockers, sequencing constraints, and prerequisites, paired with mitigation, a needed decision, or a monitoring signal when known.
- **Non-Goals** — Exclusions needed to prevent likely scope drift or false expectations.
- **Assumptions and Unknowns** — Unresolved evidence gaps that affect direction or confidence.
- **Decisions and Changes** — Significant decisions or revisions with rationale and impact.

Omit optional sections that would be empty or generic. When evidence is unavailable, state a material gap and its consequence briefly; do not fabricate detail to fill the template.

## Track Milestone Progress

Use Markdown task checkboxes for milestones only:

- `- [ ]` means the milestone is planned, underway, or otherwise not yet verified complete.
- `- [x]` means evidence verifies the stated outcome. Add a concise evidence link or note when completion is not obvious from repository state.
- Preserve known checkbox state during revisions. Never infer completion from activity alone; reopen a milestone if later evidence invalidates it.
- Add a brief status label such as `_(In progress)_` only when the distinction is useful. Do not invent percentages.

Checkboxes track strategic milestone outcomes, not implementation tasks. Use `write-plans` when a milestone must be decomposed into executable work.

## Check Strategic Coherence

Before handoff, verify that:

- Vision → objectives → milestones → success measures form a traceable chain; include themes only when they clarify that chain.
- Each phase has a distinct outcome, logical dependencies, and a credible transition to the next phase.
- Technical-health work appears in the phases that need it rather than becoming an unsequenced side list.
- Material risks distinguish uncertainty from dependency and include mitigation, a decision, or a monitoring signal when possible.
- Measures reflect outcomes rather than output volume, and unsupported targets remain explicit unknowns.
- Optional sections earn their space, meaningful boundaries are clear, and significant prior decisions are preserved without inventing history.

## Revise and Hand Off

When revising, preserve verified milestone status and prior significant decisions, then update affected objectives, phases, risks, measures, and boundaries so the roadmap remains internally consistent.

Lead with the completed roadmap or review verdict. Follow only with material assumptions, evidence gaps, or decisions still required.

## Delete Completed Roadmaps

Delete a completed saved roadmap, then report the deleted path.
Treat the roadmap as complete only when every milestone has valid completion evidence and material unknowns, risks, dependencies, and handoff decisions have a clear disposition.
Do not delete a chat-only roadmap or a roadmap with missing completion evidence.
