# Advanced Layouts

Use these only when a simple title/list slide is not enough.

## Split Layout

```markdown
![bg right:45% fit](assets/diagram.svg)

# Left Column

- Explanation
- Tradeoff
- Result
```

Swap `right` for `left`, or tune the width with `right:40%`.

## Full-Bleed Background

```markdown
![bg cover](assets/background.jpg)

<!-- _color: white -->

# Overlay Title
```

Add a darkened image variant when text contrast fails; do not rely on low-contrast overlays.

## Three-Column Comparison

```markdown
# Options

| A | B | C |
| --- | --- | --- |
| Fast | Safe | Cheap |
| Risk | Cost | Limit |
```

If the table feels dense, split it into three slides.

## Dashboard / Metrics

```markdown
# Results

| Metric | Value |
| --- | ---: |
| Latency | 42 ms |
| Errors | 0.1% |
```

Prefer one headline metric plus two supporting metrics.

## Mixed Code and Diagram

Use a split background SVG plus a short code block. If either side needs shrinking below readable size, make two slides.
