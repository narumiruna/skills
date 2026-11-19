# Agent Skills format and naming

Use the [Agent Skills specification](https://agentskills.io/specification) as the authority for the portable format.
Check the target client separately for discovery locations and client-specific extensions.

## Check the format

A skill needs a directory containing a case-sensitive `SKILL.md` with YAML frontmatter followed by Markdown instructions.

| Field | Rule |
| --- | --- |
| `name` | Required; 1–64 characters and an exact match for the directory name. Use lowercase letters, digits, and single hyphens, with no leading or trailing hyphen. |
| `description` | Required; 1–1024 characters. Describe both the work and when to load the skill. |
| `license` | Optional license name or path to a bundled license file. |
| `compatibility` | Optional; 1–500 characters when present. Include only real runtime, package, network, or client requirements. |
| `metadata` | Optional mapping with string keys and string values. |
| `allowed-tools` | Experimental, optional space-separated list of pre-approved tools. Do not assume the target client supports it. |

Keep `SKILL.md` under 500 lines and aim for fewer than 5,000 tokens in its body; these are recommendations, not format limits.
Link resources directly from `SKILL.md` using paths relative to the skill root, rather than requiring the agent to follow a chain of files.
Check that each path resolves to an existing file inside the skill directory.
The reference CLI checks frontmatter and naming conventions; it does not verify resource links or client behavior.
The bundled CLI comes from [Agent Skills upstream at `83021e2`](https://github.com/agentskills/agentskills/tree/83021e2be457a9b6679148719c1f6074f0ad975e/skills-ref) under Apache-2.0.
The local copy adds Python script metadata for repository linting without changing validation behavior.

## Choose a name

- Prefer a base-form action verb and a specific object in lowercase kebab-case, such as `write-proofs` or `generate-release-notes`.
- Add a product or tool name only when it helps distinguish the trigger, as in `lean-write-proofs` or `lean-verify`.
- Preserve the user's meaning instead of forcing a pattern, and avoid vague terms like `helper` or `utils`.
- Check nearby names and exact-name references before recommending a name.

## Rename an existing skill

Update the directory, frontmatter, and affected catalog or discovery configuration together.
Search for the old name in links, examples, commands, and checks, and update references that should point to the new name.
Keep a compatibility note if outside users still depend on the old name.
