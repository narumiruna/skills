---
name: write-agent-skills
description: Create and maintain Agent Skills. Use when turning a repeatable workflow into a skill, choosing a skill name, or revising, renaming, reviewing, or validating a skill. This includes fixing discovery, activation, and workflow. Score or numerically compare skills only on explicit request.
---

# Write Agent Skills

## Create or maintain a skill

1. Read the target repository's rules, nearby skills, discovery configuration, and any model guide that explicitly covers the target model.
   Use the repository's scaffold if it has one.
2. Define the task, the result, and what is outside the skill's scope.
   Start from a successful run, user corrections, or reliable project artifacts such as runbooks, schemas, and failure reports.
   When fixing an existing skill, reproduce the reported problem if practical.
   Ask one question only if the purpose, trigger, or location cannot be determined safely.
3. Choose a name and check the frontmatter against the [format and naming rules](references/format-and-naming.md).
   Write the description around user intent: say what the skill does and when to load it.
   Use terms users actually use and distinguish the nearest tasks that do not need the skill.
4. Write the procedure the agent follows after loading the skill.
   - Keep one sentence per line.
   - Teach reusable steps and non-obvious constraints rather than generic advice or steps that fit only one example.
   - Give a clear default and the conditions for using an alternative.
   - Prescribe the order, approvals, and checks for fragile or irreversible steps; leave flexible decisions to the agent.
   - State what evidence proves the task is done and where to stop.
   - Keep critical rules in `SKILL.md` and link optional material directly with a condition for loading it.
5. Add supporting files only when they have a job.
   - Use `references/` for details needed on demand and `assets/` for templates or other files used in outputs.
   - Read [script design](references/script-design.md) when adding or changing a command or moving repeatable logic into `scripts/`.
   - Keep bundled files inside the skill directory; this boundary does not restrict task inputs, outputs, or files in the target repository.
   - Do not add a separate README, changelog, or installation guide unless the framework needs it.
6. Change the catalog or installation configuration only where the repository uses it for discovery and the change affects it.

## Validate and report

- Run the target repository's checker and required gate for changes.
- For the portable Agent Skills format, run the [bundled skills-ref CLI](scripts/skills-ref/pyproject.toml) with `uv` and Python 3.11 or later.
  Set `skill_root` to the absolute path of this skill and `target_dir` to the directory being checked.
  Use the local source in editable mode so validation picks up changes to the bundled CLI.
  The first run may download dependencies.

  ```bash
  uv run --no-project --with-editable "$skill_root/scripts/skills-ref" \
    python -B -m skills_ref.cli validate "$target_dir"
  ```

  Use the [format and naming rules](references/format-and-naming.md) to verify optional field contents and bundled links separately.
- Exercise changed scripts on safe, realistic inputs.
- Read [skill evaluation](references/evaluate-skills.md) when creating a skill, changing its trigger or workflow, or investigating a behavioral failure.
  Check discovery, activation, and output separately; a format check cannot verify them.
- Report what changed, which checks ran, and which failed or could not run.
  Do not claim runtime behavior without observing it.

## Handle requests that do not authorize edits

Suggesting names, reviewing, and scoring are read-only unless the user also asks for changes.
Use only non-mutating checks for read-only requests.

- For name suggestions, use the [naming rules](references/format-and-naming.md#choose-a-name) and lead with one recommendation and its main reason.
  When asked to rename, follow the [rename checks](references/format-and-naming.md#rename-an-existing-skill).
- For review, lead with findings in order of importance and give evidence and a concrete fix for each.
- Keep numerical ratings and rankings out of normal reviews unless explicitly requested.

Make requested local edits and safe checks without extra approval.
Ask before external writes, destructive or costly actions, or a material increase in scope.
