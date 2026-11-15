# Themes and Directives

Use Marp's built-in themes unless the deck already carries a custom theme.

## Built-In Themes

- `default`: neutral docs and technical decks.
- `gaia`: presentation-style slides with stronger defaults.
- `uncover`: centered keynote-style slides.

```yaml
---
marp: true
theme: default
paginate: true
---
```

## Common Classes

```markdown
<!-- _class: lead -->
# Centered lead slide

---

<!-- _class: invert -->
# Dark variant

---

<!-- _class: lead invert -->
# Centered dark divider
```

## Local Styling

Use scoped style blocks sparingly and keep them close to the slide they affect.

```markdown
<style scoped>
section { background: #111827; color: #F9FAFB; }
strong { color: #FBBF24; }
</style>

# Highlighted Slide
```

## Headers and Footers

```markdown
<!-- header: Project Name -->
<!-- footer: Confidential -->
```

Avoid headers/footers on dense slides.

## Color Rule

Set a palette once, then reuse it. Do not invent a new color for each slide.
