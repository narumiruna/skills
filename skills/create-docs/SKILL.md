---
name: create-docs
description: Create a new architecture decision record (ADR), request for comments (RFC), product requirements document (PRD), project README, glossary, contributor guide (CONTRIBUTING.md), issue draft, or pull request draft from a Markdown template. Use only when the target document does not already exist. Do not use to revise or review an existing document.
---

# Create Docs

## Choose the document

Use the document type the user requests, or choose one by the outcome they need.

| Outcome | Template | Default output if the project has no convention |
| --- | --- | --- |
| Preserve a specific architecture decision and why it was made | [ADR](assets/ADR.md) | `docs/decisions/NNNN-title-with-dashes.md` |
| Propose a change and ask reviewers for feedback | [RFC](assets/RFC.md) | `docs/rfc/<topic>.md` |
| Define a user problem, product requirements, and how to verify them | [PRD](assets/PRD.md) | `docs/prd/<topic>.md` |
| Explain what a project or package does and help a reader get started | [README](assets/README.md) | `README.md` at the project or package root |
| Define shared project terms and distinguish similar concepts | [Glossary](assets/GLOSSARY.md) | `GLOSSARY.md` at the project or package root |
| Explain how to report issues, verify changes, and contribute | [Contributor guide](assets/CONTRIBUTING.md) | `CONTRIBUTING.md` at the repository root |
| Report a problem, request a change, or track work | [Issue](assets/ISSUE.md) | Draft in chat |
| Explain a change and how you verified it for reviewers | [Pull request](assets/PULL_REQUEST.md) | Draft in chat |

Use `write-plans` for an implementation task list and `write-agents-md` for agent instructions instead.

## Check that the document is new

Before reading a template, check the requested path and look for the target document where the project keeps documents of that type.
For a contributor guide, also check for existing `CONTRIBUTING` files at the repository root and in `.github/` and `docs/`, regardless of case or file extension.
Use the default output only when neither the user nor the project specifies one.
If the target document already exists, report its path and stop without overwriting it or creating a duplicate.
For the default ADR path, use the next four-digit number (start at `0001`) and a lowercase title with hyphens.

## Create the document

1. Identify the audience and what the reader should know or do after reading.
   Inspect nearby examples and relevant sources such as code, configuration, or decisions supplied by the user.
2. Follow the project's templates, naming, numbering, and status conventions.
   Read only the matching bundled template if no project template applies or if it leaves gaps.
   Include sections marked `(optional)` only when their prompts apply, and remove the marker from headings you keep.
3. Put the most important information first.
   Use project terms consistently and separate current behavior, proposals, confirmed decisions, and open questions.
   Do not invent approvals, requirements, metrics, commands, or definitions.
   When a material fact is missing, identify it as unresolved instead of treating it as settled.
4. Replace every required placeholder.
   Fill optional placeholders only when a value applies; otherwise remove them and any text or markup used only for those fields.
   Remove unused sections and template comments.
   Check local links, verify technical claims against sources, and run only safe, non-destructive examples when practical.
   Say what could not be verified.
5. Return the draft in chat or create the new local document, as determined above.
   Do not implement or publish a change as part of drafting.
   Do not post an issue or open a pull request.
