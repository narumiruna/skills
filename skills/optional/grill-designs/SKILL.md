---
name: grill-designs
description: Interview the user one decision at a time to stress-test a plan or design until goals, constraints, assumptions, tradeoffs, risks, and verification are explicit. Use only when the user asks to be grilled or names “grilling designs.”
---

# Grilling Designs

Build a live decision tree from the user's goal, constraints, stakeholders, flows, dependencies, risks, and success criteria.

## Loop

1. Resolve answers available from repository files, callers, configuration, docs, tests, or commands before questioning the user.
2. Select the highest-leverage unresolved decision that unlocks later branches.
3. Ask exactly one question with:
   - **Question:** the one decision needed next.
   - **Options:** a numbered list of credible choices.
   - **Recommended answer:** the option you recommend and the deciding rationale.
4. Incorporate the answer, resolve dependent branches, and repeat. If it conflicts with evidence or an earlier decision, state the conflict and ask the smallest clarifying question.

Prioritize goal/success, constraints/non-goals, architecture facts, interfaces/data/state ownership, failure/security/migration/rollout/observability, then test and verification criteria.

Do not draft a plan while major branches remain. When the user requests a plan after the interview, use `write-plans` with the agreed decisions.

Stop when no major unresolved branch remains. Return the agreed decisions, remaining risks or unknowns, and the recommended next action.
