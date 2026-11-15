# SVG Pattern Examples

Use these structures as starting points; keep palette and sizing consistent within a deck.

## Process Flow

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 180">
  <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#2563EB"/></marker></defs>
  <g font-family="Arial, sans-serif" font-size="18" text-anchor="middle">
    <rect x="20" y="50" width="160" height="80" rx="16" fill="#DBEAFE" stroke="#2563EB" stroke-width="3"/>
    <text x="100" y="98">Input</text>
    <line x1="180" y1="90" x2="300" y2="90" stroke="#2563EB" stroke-width="3" marker-end="url(#arrow)"/>
    <rect x="300" y="50" width="160" height="80" rx="16" fill="#DBEAFE" stroke="#2563EB" stroke-width="3"/>
    <text x="380" y="98">Process</text>
  </g>
</svg>
```

## Architecture Cards

```xml
<g font-family="Arial, sans-serif">
  <rect x="40" y="40" width="260" height="140" rx="16" fill="#F8FAFC" stroke="#CBD5E1" stroke-width="3"/>
  <text x="70" y="90" font-size="24" font-weight="700" fill="#0F172A">Service</text>
  <text x="70" y="126" font-size="16" fill="#475569">Responsibility</text>
</g>
```

## KPI Tile

```xml
<g font-family="Arial, sans-serif">
  <rect width="240" height="140" rx="16" fill="#111827"/>
  <text x="24" y="52" font-size="18" fill="#9CA3AF">Latency</text>
  <text x="24" y="104" font-size="44" font-weight="700" fill="#F9FAFB">42ms</text>
</g>
```

## Adaptation Rules

- Duplicate groups instead of inventing new styles.
- Change labels first, then dimensions.
- Re-run SVG validation after editing XML.
