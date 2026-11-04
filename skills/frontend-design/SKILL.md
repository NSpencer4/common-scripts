---
name: frontend-design
description: >-
  Distinctive, intentional frontend visual design for new or reshaped UI.
  Combines anti-slop art direction, typography/layout discipline, and a
  look-and-fix critique loop. Use when building, redesigning, polishing, or
  reviewing landing pages, marketing surfaces, product pages, heroes, or
  public-facing web UI — or when a page looks generic, templated, or "AI-made".
  For reusable component libraries and Storybook, also use atomic-presentational-ui.
  No bundled design scripts; the agent deals directions and inspects with available
  browser/screenshot tools.
---

# Frontend Design

Act as a design lead who refuses templated AI defaults. Every brief gets a
specific point of view: palette, type, layout, and imagery rooted in the
**subject**, not in whatever the model generates by habit.

This skill merges Anthropic frontend-design guidance, taste-skill house rules
(without its Node/Chrome scripts), and standing product hard rules below.
Repository design systems and existing brand tokens win when they conflict.

For reusable component APIs and Storybook catalogs, pair with
`atomic-presentational-ui`. Do not replace an established component library with
a one-off marketing kit.

## Hard product rules

Apply these on branded/marketing surfaces unless the repo already mandates otherwise:

- **One composition** in the first viewport (not a dashboard, unless it is one)
- **Brand first**: brand/product name is hero-level, not a nav leftover
- **Brand test**: if removing the nav makes the first viewport feel unowned, branding is too weak
- **Expressive type**: avoid Inter / Roboto / Arial / system as the design voice
- **Atmosphere**: avoid flat single-color grounds; use gradient, image, or subtle pattern with intent
- **Full-bleed hero** on landing/promotional surfaces by default; no inset hero cards or floating media collages unless the system requires it
- **Hero budget**: brand, one headline, one short support line, one CTA group, one dominant image — no stats/schedules/promo clutter in the first viewport
- **No hero overlays**: no floating badges, chips, or stickers on hero media
- **Cards**: default off; never in the hero; only when they contain a real interaction
- **One job per section**
- **Real visual anchor**: product/place/atmosphere imagery beats abstract decoration as the main idea
- **Motion**: 2–3 intentional moments, not noise
- **Avoid default AI looks**: purple-on-white / purple-indigo gradients; warm cream (#F4F1EA) + terracotta; broadsheet hairline / zero-radius newspaper cosplay; unearned dark mode; glow stacks; pill clusters; emoji ornament

App/dashboard screens follow quieter rules (see `references/app-screens.md`):
borders and repeated panels are normal; vanity charts, rainbow accents, and
fake metrics are not.

## Process

### 1. Ground in the subject

Name the product/subject, audience, and primary job of the page. If unclear,
propose one concrete reading and confirm. Distinctiveness comes from the
subject's materials and vernacular, not from a generic "premium SaaS" costume.

### 2. Deal a direction (no scripts)

Without the upstream `draw.mjs` binary, invent **three** sharply different
directions yourself, then pick one with the user (or state the pick if AFK).

Each direction must state:

- **Idea**: one sentence tied to the subject (not "clean modern")
- **Composition**: hero treatment + section rhythm (ASCII wireframe welcome)
- **Type**: one family or two clearly distinct families; roles for display/body
- **Palette**: 4–6 named hex values with jobs (ground, ink, accent, support…)
- **Imagery plan**: real photos, product UI crop, illustration, or none — and why

Prefer directions that would fail a "could this be any other brand?" test.

### 3. Review the plan against tells

Before coding, scrub the plan using `references/tells.md` and the hard rules.
If any axis looks like the default you would produce for any similar brief,
revise it and say what changed.

Also avoid Anthropic-noted defaults: single-word headline accents, ALL-CAPS
labels as chrome, unnecessary eyebrows, identical card grids, soft grey shadow
kits, gradient washes as decoration.

### 4. Build

Implement against the locked plan. Prefer host design tokens when building
inside an existing app. Keep CSS specificity sane; don't let utility classes
fight element rules into a mess.

Write copy as design content: active voice, sentence case, same action name
through a flow, specific empty/error states. See `references/copy.md`.

### 5. Critique loop

If browser/screenshot tools exist, capture desktop and mobile, then critique
with `references/critique.md`. Fix the worst issue, look again. Without
screenshots, still do a structured self-critique against tells, hero budget,
and brand test.

Spend boldness in one place; remove one accessory before shipping the pass.

## House style pointers

| Topic | Reference |
|-------|-----------|
| Banned/warned tells | `references/tells.md` |
| Colour | `references/colour.md` |
| Type | `references/type.md` |
| Layout | `references/layout.md` |
| Imagery | `references/imagery.md` |
| Motion | `references/motion.md` |
| Copy | `references/copy.md` |
| Critique rubric | `references/critique.md` |
| App screens | `references/app-screens.md` |
| Research notes | `references/research.md` |

When references mention upstream inspector/lint scripts, **do not expect those
binaries**. Perform the same checks manually or with available browser tools.

## Restraint

Removal of tells is not enough: replace them with substance (strong type, real
imagery, decisive colour fields, complete section content). An empty "clean"
page loses to a richer page that still has tells.

## License notes

Anthropic frontend-design portions: see `LICENSE-anthropic.txt`. Taste-skill
reference material was snapshotted as static markdown without its executable
scripts.
