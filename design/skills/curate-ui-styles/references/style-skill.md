# Saved style skill format

The canonical file is `ui-styles/ui-style-<id>/SKILL.md` relative to the selected workspace.
Use a lowercase kebab-case ID and keep the full directory name at most 64 characters.
Keep one style per directory and make the frontmatter name match it.
Use the user's language for style rules and include the style's name in the description.

Start with this structure and remove unused headings:

```markdown
---
name: ui-style-<id>
description: "Apply the <Style name> UI style to <scope>. Use only when the user selects this style by name or path."
---

# <Style name>

Use this style only when explicitly selected.
Apply it to <surfaces and scope>.
Keep product behavior, accessibility, and fixed project requirements intact.

## Overall

- <Confirmed screen composition, rhythm, or emphasis.>

## Components

- <Confirmed component treatments and relevant states.>

## Details

- <Confirmed values or relative rules, with their semantic roles and scope.>
```

Use exact values where the user confirmed them in a preview or reply.
For example, write “Use a 12px radius for cards; keep the existing button radius” rather than “use friendly shapes everywhere.”
Resolve potential conflicts at the narrowest scope the user confirmed.
Do not add fallback values, preferences, or wider scope based only on design taste.
Omit interview history, option letters, draft references, and temporary preview paths from the saved skill.

## Manage and reuse

- **List or show:** Read saved skills from the chosen catalog and show their names, scope, and paths without editing them.
- **Compare:** Load the selected style skills and render them on the same screen under the same content and viewport constraints.
  Label differences and note any missing rules instead of attributing preview defaults to the skills.
- **Copy:** Confirm the source and destination, require an unused ID, and change the human title and the frontmatter name and description in the copy.
- **Refine:** Preserve all rules unrelated to the confirmed change and check that the base file has not changed since the draft was started before writing.
  If it changed, review the overlap before overwriting any rule.
- **Reuse:** Give the agent the saved `SKILL.md` path and name the style to apply.
  For explicit invocation by name, export the style into a discovery location the user has chosen and follow that client's reload or restart process.
  Do not assume the catalog itself is automatically discovered.
- **Undo or remove:** Prefer a copy before a broad rewrite and use existing version control for history where available.
  Do not delete or overwrite another style without explicit confirmation.
