# Color Design Workflow

Produce a slide-ready semantic palette with measured contrast and honest environment caveats.

## 1. Establish Context

Identify the audience, content type and density, tone, existing brand or theme, and delivery conditions. When missing context affects the choice, state an assumption rather than presenting it as known.

## 2. Choose a Strategy

Use `strategies.md` for detailed tradeoffs:

| Strategy | Typical fit | Main risk |
| --- | --- | --- |
| Dark Technical | code, terminals, diagrams, controlled light | washout in bright rooms or print |
| Light Professional | formal, text/data, bright rooms, handouts | glare or weak hierarchy |
| Accent-Driven | storytelling and selective emphasis | overuse or insufficient data-series distinction |

Treat these as starting points, not rigid audience rules.

## 3. Define Semantic Roles

Define:

- Background
- Surface
- Primary
- Secondary
- Accent
- Text Primary
- Text Secondary

Roles describe use, not necessarily seven unique colors. Reuse a value when the roles remain understandable. Add Success, Warning, Error, or chart-series colors only when the content needs them; never rely on color alone for meaning.

For each role, provide a hex value, purpose, and relevant foreground/background pairing. Preserve supplied brand colors and adapt surrounding roles when a brand value cannot serve accessible text.

## 4. Measure Actual Pairings

Calculate every text/background combination that the deck will use. Apply the relevant WCAG contrast target—normally at least 4.5:1 for body text and 3:1 for qualifying large text—and record the ratio. Aim higher when venue or typography risk justifies it.

Contrast is necessary but does not prove projector, print, recording, or venue performance. Those checks require the exported artifact and target condition.

## 5. Define Usage

Specify only applicable rules for:

- title and section slides
- body text and metadata
- surfaces and code blocks
- diagrams and connectors
- charts and semantic states

Use color to reinforce hierarchy established through layout and typography. Limit accent use so it retains meaning.

## 6. Validate and Hand Off

When a deck exists, apply the palette to representative title, dense-content, data/code, and visual slides. Check role consistency, color-independent meaning, clipping, and relevant delivery conditions.

Use `output-template.md` for the handoff. Mark only checks supported by direct evidence; leave unavailable environment checks open and name what remains.
