---
name: create-mermaid-diagrams
description: Create, revise, convert, or validate Mermaid diagrams, including flowcharts, sequence, ER, class, state, Gantt, and optional SVG rendering for documents or slides.
---

# Mermaid Diagrams

Preserve editable Mermaid source. Temporary renders used only for validation are allowed; preserve or deliver a static asset only when the consumer requires one.

## Route by Structure

| Type | Best for | Basic source |
| --- | --- | --- |
| Flowchart | processes and decisions | `assets/examples/flowchart/basic.mmd` |
| Sequence | ordered system interactions | `assets/examples/sequence/basic.mmd` |
| Class | object models | `assets/examples/class/basic.mmd` |
| State | lifecycle transitions | `assets/examples/state/basic.mmd` |
| ER | data entities and relationships | `assets/examples/er/basic.mmd` |
| Other | Gantt, pie, git, journey, timeline, mindmap, requirement, C4 | `assets/examples/other/gantt-basic.mmd` |

Read `references/types.md` only for type-specific decisions or syntax beyond the basic source.

## Workflow

1. Identify the relationships, sequence, or states the diagram must communicate and choose the matching type.
2. Write one focused `.mmd` source with descriptive labels and simple alphanumeric or underscore IDs. Split a graph that becomes unreadable.
3. Validate with the consumer's Mermaid renderer when known. Otherwise, use Mermaid CLI when available:

```shell
mmdc -i diagram.mmd -o /tmp/diagram-check.svg
```

4. If a slide or document needs a static asset, render the requested SVG with an appropriate theme, background, and dimensions, then inspect it in the target artifact.
5. Return or preserve the source, any requested rendered artifact, validation performed, and renderer/version compatibility caveats.

Quote labels containing punctuation. Prefer high contrast for slides. Diagram creation does not authorize a Git commit or publication.
