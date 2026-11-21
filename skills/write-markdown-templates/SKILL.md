---
name: write-markdown-templates
description: Create or revise reusable Markdown document templates, including their filenames, sections, placeholders, and writing prompts. Use when the output is a template, not a finished document filled from one.
---

# Write Markdown Templates

## Identify the output

Identify the document type, who fills it in, and what each finished document must contain.
Inspect the intended destination, nearby templates, and any instructions or code that use the template.
Create or revise the template itself; do not fill it in or introduce a template engine.

## Name and place the file

1. Follow the requested path, any filename required by a tool, and the project's existing naming and location conventions.
   When revising a template, keep its current path unless the user requests a rename.
2. Otherwise, name the template after the document it produces: use a lowercase kebab-case basename and a `.md` extension, such as `adr.md` or `bug-report.md`.
   Prefer the document type even if it is the only template; omit redundant prefixes or suffixes such as `template-` and `.template`.
3. For an Agent Skill, put the template in the consuming skill's `assets/` and link to it from that skill's `SKILL.md`.
   For other projects with no convention, use `templates/` at the project root.
4. If a request to create a template would overwrite an existing file, report the path and stop unless the user also requests a revision.

## Write the template

Use the [Markdown template scaffold](assets/markdown-template-scaffold.md) for a new template when the project has no scaffold.
Replace its sample headings and prompts with ones specific to the document.

- Put required sections in reading order and add optional sections only when they cover a distinct need.
  Mark those headings `(optional)` and explain when to include them.
- Use descriptive `[Placeholder]` text for values that need to be replaced.
  Keep the project's existing syntax when a convention or renderer requires it.
- Use HTML comments for short writing prompts.
  Tell the writer what to include or how to tell the section is complete; do not repeat the heading or add a second placeholder that says the same thing.
- Show the expected Markdown structure when it matters, such as a task checkbox or a table row.
  Do not prefill decisions or other facts that can differ between documents.

## Check and deliver

Fill a representative example in memory to check that the required sections work and that an optional section can be removed cleanly.
Check that the finished example has no unresolved placeholders, instructional comments, or `(optional)` markers.
Keep those aids in the template itself.
Verify the filename, Markdown structure, and any new or changed link to the template.
Return the template in chat if requested; otherwise write it to the intended local path.
