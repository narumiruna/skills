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

# Comprehensive Example
All features: palette + slides + diagrams + code

Tech Conference · 2026-01-09

---

## What This Demo Shows

* ✅ Custom dark technical palette
* ✅ Marpit slide patterns (title, content, two-column, code)
* ✅ Inline SVG diagrams
* ✅ Visual consistency across all elements
* ✅ Proper contrast and hierarchy

**Goal**: Show how all three modules work together.

---

<!-- _class: lead -->
<!-- _backgroundColor: #0C0C0C -->
<!-- _color: #569CD6 -->

# Section 1: Architecture

---

## System Components

<svg viewBox="0 0 700 350" xmlns="http://www.w3.org/2000/svg">
  <!-- Frontend -->
  <rect x="50" y="50" width="180" height="100" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="140" y="90" font-size="16" fill="#569CD6" text-anchor="middle" font-weight="bold">Frontend</text>
  <text x="140" y="115" font-size="12" fill="#D4D4D4" text-anchor="middle">React + TypeScript</text>

  <!-- Backend -->
  <rect x="260" y="50" width="180" height="100" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="350" y="90" font-size="16" fill="#569CD6" text-anchor="middle" font-weight="bold">Backend</text>
  <text x="350" y="115" font-size="12" fill="#D4D4D4" text-anchor="middle">Node.js + Express</text>

  <!-- Database -->
  <rect x="470" y="50" width="180" height="100" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="560" y="90" font-size="16" fill="#569CD6" text-anchor="middle" font-weight="bold">Database</text>
  <text x="560" y="115" font-size="12" fill="#D4D4D4" text-anchor="middle">PostgreSQL</text>

  <!-- Cache -->
  <rect x="260" y="200" width="180" height="100" fill="#252526" stroke="#4EC9B0" stroke-width="2" rx="4"/>
  <text x="350" y="240" font-size="16" fill="#4EC9B0" text-anchor="middle" font-weight="bold">Cache</text>
  <text x="350" y="265" font-size="12" fill="#D4D4D4" text-anchor="middle">Redis</text>

  <!-- Arrows -->
  <path d="M 140 150 L 260 100" stroke="#4EC9B0" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 440 100 L 470 100" stroke="#4EC9B0" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 350 150 L 350 200" stroke="#4EC9B0" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Arrow marker -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#4EC9B0"/>
    </marker>
  </defs>
</svg>

---

## Implementation Details

```typescript
interface APIConfig {
  baseURL: string;
  timeout: number;
  retries: number;
}

class APIClient {
  private config: APIConfig;

  constructor(config: APIConfig) {
    this.config = config;
  }

  async request<T>(endpoint: string): Promise<T> {
    // Implementation with retry logic
    return fetch(`${this.config.baseURL}${endpoint}`)
      .then(res => res.json());
  }
}
```

---

## Two-Column Layout

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 48px;">

<div>

### Benefits

* High performance
* Easy to scale
* Modular architecture
* Type-safe frontend

</div>

<div>

### Challenges

* Initial setup complexity
* Cache invalidation
* Database migrations
* Monitoring overhead

</div>

</div>

---

<!-- _class: lead -->
<!-- _backgroundColor: #0C0C0C -->
<!-- _color: #569CD6 -->

# Section 2: Performance

---

## Response Time Metrics

<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <!-- Axes -->
  <line x1="60" y1="250" x2="560" y2="250" stroke="#858585" stroke-width="2"/>
  <line x1="60" y1="50" x2="60" y2="250" stroke="#858585" stroke-width="2"/>

  <!-- Y-axis labels -->
  <text x="45" y="55" font-size="12" fill="#858585" text-anchor="end">200ms</text>
  <text x="45" y="155" font-size="12" fill="#858585" text-anchor="end">100ms</text>
  <text x="45" y="255" font-size="12" fill="#858585" text-anchor="end">0ms</text>

  <!-- X-axis labels -->
  <text x="120" y="270" font-size="12" fill="#858585" text-anchor="middle">Q1</text>
  <text x="240" y="270" font-size="12" fill="#858585" text-anchor="middle">Q2</text>
  <text x="360" y="270" font-size="12" fill="#858585" text-anchor="middle">Q3</text>
  <text x="480" y="270" font-size="12" fill="#858585" text-anchor="middle">Q4</text>

  <!-- Bars -->
  <rect x="100" y="150" width="40" height="100" fill="#569CD6"/>
  <rect x="220" y="120" width="40" height="130" fill="#569CD6"/>
  <rect x="340" y="180" width="40" height="70" fill="#4EC9B0"/>
  <rect x="460" y="195" width="40" height="55" fill="#4EC9B0"/>

  <!-- Legend -->
  <rect x="480" y="80" width="20" height="20" fill="#569CD6"/>
  <text x="510" y="95" font-size="12" fill="#D4D4D4">Before optimization</text>
  <rect x="480" y="110" width="20" height="20" fill="#4EC9B0"/>
  <text x="510" y="125" font-size="12" fill="#D4D4D4">After optimization</text>

  <!-- Highlight -->
  <text x="390" y="170" font-size="14" fill="#F4BF75" font-weight="bold">-60%</text>
</svg>

**Result**: 60% improvement in Q3-Q4 after cache implementation

---

## Key Optimizations

1. **Database Connection Pooling**
   - Reduced connection overhead
   - 40% faster queries

2. **Redis Caching**
   - 5-minute TTL for frequent queries
   - 80% cache hit rate

3. **Code Splitting**
   - Lazy loading for routes
   - 50% smaller initial bundle

---

<!-- _class: lead -->
<!-- _backgroundColor: #0C0C0C -->
<!-- _color: #569CD6 -->

# Summary

---

## What We Built

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 32px;">

<div>

<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="160" height="110" fill="#252526" stroke="#569CD6" stroke-width="2" rx="4"/>
  <text x="100" y="80" font-size="16" fill="#569CD6" text-anchor="middle" font-weight="bold">System</text>
</svg>

**Architecture**: Modular and scalable

</div>

<div>

<svg viewBox="0 0 200 150" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="160" height="110" fill="#252526" stroke="#4EC9B0" stroke-width="2" rx="4"/>
  <text x="100" y="80" font-size="16" fill="#4EC9B0" text-anchor="middle" font-weight="bold">Performance</text>
</svg>

**Speed**: 60% faster responses

</div>

</div>

---

<!-- _class: lead -->
<!-- _backgroundColor: #0C0C0C -->
<!-- _color: #569CD6 -->

# Thank You

Questions?

contact@example.com

---
