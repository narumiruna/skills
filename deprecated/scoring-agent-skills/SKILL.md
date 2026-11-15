---
name: scoring-agent-skills
description: Deprecated compatibility reference for numerical agent-skill ratings and rubric-based comparisons. Use the active write-agent-skills workflow for current skill scoring, review, revision, and creation work.
metadata:
  internal: true
---

# Scoring Agent Skills (Deprecated Reference)

Use `write-agent-skills` for the maintained workflow. Its explicitly requested Score mode preserves the former `$scoring-agent-skills` behavior and owns the current six-dimension rubric.

Do not score an ordinary review unless the user explicitly asks for ratings, numerical scores, a rubric, or a scored comparison. A scoring request remains read-only unless revisions are also requested.

For compatibility, establish the target-model baseline, inspect the skill and its relevant discovery and resource surfaces, apply the same rubric anchors to every assessed skill, support scores with direct evidence, and separate structural validation from qualitative judgment. Mark materially unavailable dimensions unassessed rather than inventing evidence.

Report the scope, baseline, dimension scores, one-decimal aggregate with coverage, evidence-based notes, validation evidence, and improvement priorities. State that source-and-structure scoring is not a runtime effectiveness benchmark.
