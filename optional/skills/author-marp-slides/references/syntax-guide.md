# Marp/Marpit Syntax Guide

Use this as the minimum syntax checklist before writing slides.

## Required Structure

```markdown
---
marp: true
theme: default
paginate: true
---

# Title

---

## Slide title

Body text.
```

Rules:

- Start with YAML frontmatter and `marp: true`.
- Separate slides with `---` on its own line.
- Use one `#` title per slide; use `##` and lists for body structure.
- Keep speaker notes in HTML comments only if the renderer supports them.

## Directives

Global directives live in frontmatter. Per-slide directives use HTML comments before the slide content.

```markdown
<!-- _class: lead invert -->
<!-- _backgroundColor: #111827 -->
<!-- _color: #F9FAFB -->
```

Common directives: `theme`, `paginate`, `size`, `class`, `backgroundColor`, `color`, `header`, `footer`.

## Images

Prefer background image syntax; it avoids manual resizing.

```markdown
## Request flow: client → gateway → service

![bg right:45% fit](assets/architecture.svg)
```

A meaningful background needs an adjacent semantic equivalent because CSS backgrounds do not expose reliable alt text. Use descriptive host-level alt text for inline images:

```markdown
![Company logo w:600](assets/logo.svg)
```

## Code

````markdown
```python
def hello() -> str:
    return "world"
```
````

Rules:

- Add a language for highlighting.
- Keep code blocks short enough to read on a slide.
- Move long examples to a repo file and show the relevant excerpt.

## Tables

Use Markdown tables only for small comparisons. For dense data, simplify or use a chart/SVG.

## Validation

Resolve `scripts/check_marpit_structure.sh` against the `author-marp-slides` skill directory and run its limited structural precheck:

```shell
AUTHORING_MARP_SLIDES_SKILL_DIR="/absolute/path/to/author-marp-slides"
bash "$AUTHORING_MARP_SLIDES_SKILL_DIR/scripts/check_marpit_structure.sh" deck.md
```

The precheck does not parse YAML or Marp syntax. Export with the actual Marp renderer as described in `preview-workflow.md`, verify directives took effect, and report strict-YAML, renderer, and visual evidence separately.
