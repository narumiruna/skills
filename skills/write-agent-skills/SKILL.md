---
name: write-agent-skills
description: Create, name, rename, revise, or review agent skills for clear triggers, safe workflows, strong checks, lean content, and easy discovery, and score or numerically compare skills only when the user explicitly asks.
---

# Writing Agent Skills

Create, name, rename, revise, review, or explicitly score a skill that another agent can find and use with little extra context.
A review or score request is read-only unless the user also asks for changes.

## Writing Rules

- Keep documents concise and clear.
- Put one sentence on each line.

## Choose the Mode

- Use Build to create, revise, optimize, or convert a workflow.
- Use Name or Rename to choose or change a skill name.
- Use Review to check a skill without numerical ratings.
- Use Score to give numerical ratings only when the user explicitly asks for them.

Do not turn a normal review into a scorecard.

## Name or Rename

Name the task and trigger that the skill represents instead of naming its implementation.

- Read the description and workflow to find the action, subject, domain, and any needed product name.
- Use lowercase kebab-case and a base-form action verb, not its `-ing` form.
- Prefer `verb-object`, such as `write-proofs` or `review-code`.
- Add a tool prefix only when it clarifies the skill’s scope or distinguishes it from similar skills, such as `lean-write-proofs`.
- Allow `tool-verb`, such as `lean-verify`, when the tool and action make the task clear without an object.
- Allow multiword objects, such as `generate-release-notes`.
- Use meaningful digits only when needed.
- Use single hyphens, and do not put a hyphen at either end.
- Keep the directory name and frontmatter `name` the same, and follow the framework's length limit.
- Avoid vague words such as `helper`, `utils`, `tools`, `assistant`, `magic`, `smart`, and `general`.
- Use a product or organization name only when the trigger truly depends on it.
- Preserve the user's meaning instead of forcing the preferred naming pattern.
- Check nearby names and exact-name references, then compare a few choices for clarity, searchability, lasting value, and conflicts.
- Lead with one recommended name and its main reason.

A naming recommendation does not give permission to rename files.
Do not edit files when the user asks only for names or a review.
For an approved rename, update the directory, frontmatter, catalog, links, examples, checks, and other exact-name references in one focused change.
Keep a compatibility note when outside users still depend on the old name.
For one skill, lead with the recommended name and reason; for several skills, use a current, recommended, and reason table.
List only conflicts or compatibility work that affects use.

## Build or Review

1. Read the repository rules, skill folders, nearby skills, catalog, validators, and the model guide that applies.
2. Ask one question only when the purpose, trigger, or location is too unclear to choose safely.
3. Check the name with the rules above.
4. Keep only files with a clear job.
   - Use `SKILL.md` for the trigger and the instructions followed after the skill triggers.
   - Use `references/` for details loaded only when needed.
   - Use `scripts/` instead of prompt instructions whenever a script can do the work.
     - Keep only the guidance needed to run the script and use its output in `SKILL.md`.
   - Use `assets/` for material copied into or used by outputs.
   - Keep every bundled local document or script linked or imported by a skill file inside the directory containing `SKILL.md`; a nested resource may use `../` only when the resolved target remains inside that directory.
   - Do not apply this boundary to task inputs, outputs, target-repository files, or system paths.
   - Do not add a skill README, changelog, installation guide, or quick reference unless the framework requires it.
5. Use the repository's official scaffold when one exists, and keep edits inside the skill and required discovery files.
6. Write or check `SKILL.md` with the following rules.
   - Put `name` and a clear what-and-when `description` in supported YAML frontmatter.
   - Put trigger conditions in `description` instead of a body section about when to use the skill.
   - State each instruction once, with the result, hard limits, approval needs, required evidence, and stopping point.
   - Keep an example only when it proves a requirement or prevents a known mistake.
   - Link each resource directly, say when to use it, and do not copy its details into `SKILL.md`.
7. Update catalog or installation files only when the repository uses them for discovery.
8. For requested changes, run the documented checker, realistic examples for changed scripts, practical tests for subtle workflows, and the required repository gate.
   For review or scoring without requested changes, use only non-mutating checks; do not run auto-fix, update, or other writing hooks.
9. Report every unavailable or failing check honestly.
10. In Review mode, lead with the most important findings, show evidence, and give a clear fix for each one.
11. Make requested local edits and safe checks without extra approval.
12. Ask before external writes, destructive or costly actions, or a large increase in scope.

## Completion Criteria

- The skill has one clear purpose, an easy-to-recognize trigger, and a specific name that keeps the intended meaning.
- The body is useful only after the skill triggers, with no repeated rules, generic background, decorative examples, or files without a clear job.
- The finished document follows the writing rules above.
- Requested local edits and checks are complete, while risky or outside actions still need approval.
- Frontmatter, catalog text, resources, check results, and claims about real behavior agree.
