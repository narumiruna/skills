---
marp: true
theme: default
paginate: true
backgroundColor: #1E1E1E
color: #D4D4D4
---

<!-- _class: lead -->
<!-- _backgroundColor: #0C0C0C -->
<!-- _color: #569CD6 -->

# Example with SVG Diagram
Demonstrating diagram integration

Tech Talk · 2026-01-09

---

## System Architecture

| Layer | Example responsibility |
| --- | --- |
| Frontend | Present and validate user input |
| Backend | Apply domain behavior |
| Database | Persist durable state |

*Replace this table with an SVG only after the asset exists.*

---

## Data Flow

<svg viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="data-flow-title data-flow-desc">
  <title id="data-flow-title">Request data flow</title>
  <desc id="data-flow-desc">A request travels from the user through the API and service to the database.</desc>
  <!-- User -->
  <rect x="20" y="70" width="100" height="60" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="70" y="105" font-size="14" fill="#D4D4D4" text-anchor="middle">User</text>

  <!-- Arrow -->
  <path d="M 130 100 L 180 100" stroke="#4EC9B0" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="155" y="90" font-size="12" fill="#858585" text-anchor="middle">HTTP</text>

  <!-- API -->
  <rect x="190" y="70" width="100" height="60" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="240" y="105" font-size="14" fill="#D4D4D4" text-anchor="middle">API</text>

  <!-- Arrow -->
  <path d="M 300 100 L 350 100" stroke="#4EC9B0" stroke-width="2" marker-end="url(#arrowhead)"/>
  <text x="325" y="90" font-size="12" fill="#858585" text-anchor="middle">SQL</text>

  <!-- Database -->
  <rect x="360" y="70" width="100" height="60" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="410" y="105" font-size="14" fill="#D4D4D4" text-anchor="middle">Database</text>

  <!-- Arrow marker -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#4EC9B0"/>
    </marker>
  </defs>
</svg>

---

## Code + Diagram

```python
def process_request(data):
    # Validate input
    validated = validate(data)

    # Process business logic
    result = business_logic(validated)

    # Return response
    return result
```

**Flow visualization** matches the code structure above.

---

<!-- _class: lead -->
<!-- _backgroundColor: #0C0C0C -->
<!-- _color: #569CD6 -->

# Summary

Combining slides with inline SVG diagrams creates self-contained presentations

---
