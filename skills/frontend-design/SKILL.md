---
name: frontend-design
description: >-
  Distinctive, intentional frontend visual design for new or reshaped UI.
  Combines anti-slop art direction, typography/layout discipline, and a
  look-and-fix critique loop. Use when building, redesigning, or reviewing
  landing pages, marketing surfaces, product pages, heroes, or public-facing
  web UI, or when a page looks generic, templated, or "AI-made". Also for
  quieter app/dashboard screens (see references/app-screens.md). Own visual
  direction; defer production UI states/responsive eng to frontend-ui-engineering,
  WCAG audits to accessibility, and final micro-pass to polish. No bundled design scripts; deal directions and inspect with available
  browser/screenshot tools.
---

# Frontend Design

Act as a design lead who refuses templated AI defaults. Every brief gets a
specific point of view: palette, type, layout, and imagery rooted in the
**subject**, not in whatever the model generates by habit.

This skill merges Anthropic frontend-design guidance, leonxlnx taste-skill /
`design-taste-frontend` house rules (without Node/Chrome scripts), and standing
product hard rules below. Repository design systems and existing brand tokens
win when they conflict.

For reusable component APIs and Storybook catalogs, follow the project's
component skill if one exists. Do not replace an established component library with
a one-off marketing kit. For Stitch `DESIGN.md` work, use the Stitch design
skills; do not load this pack's retired `stitch-design-taste` as a second global
skill.

## Page or app screen

Decide first:

- **Page** (read/scroll): landing, marketing, portfolio, product, event, one-pager.
  Follow the process below plus hard product rules.
- **App screen** (worked in): dashboard, admin, analytics, settings, inbox, builder.
  Follow `references/app-screens.md` whole before starting. Quiet panels, aligned
  figures, colour spent on data; vanity charts and fake metrics are out.

A product marketing page that shows its app is still a **page**; fragments that
depict the product UI follow app-screen rules for their insides, with shared
palette and type.

## Hard product rules

Apply these on branded/marketing surfaces unless the repo already mandates otherwise:

- **One composition** in the first viewport (not a dashboard, unless it is one)
- **Brand first**: brand/product name is hero-level, not a nav leftover
- **Brand test**: if removing the nav makes the first viewport feel unowned, branding is too weak
- **Expressive type**: avoid Inter / Roboto / Arial / system as the design voice
- **Atmosphere**: avoid flat single-color grounds; use gradient, image, or subtle pattern with intent
- **Full-bleed hero** on landing/promotional surfaces by default; no inset hero cards or floating media collages unless the system requires it
- **Hero budget**: brand, one headline, one short support line, one CTA group, one dominant image. No stats/schedules/promo clutter in the first viewport
- **No hero overlays**: no floating badges, chips, or stickers on hero media
- **Cards**: default off; never in the hero; only when they contain a real interaction
- **One job per section**
- **Real visual anchor**: product/place/atmosphere imagery beats abstract decoration as the main idea
- **Motion**: 2-3 intentional moments, not noise
- **Avoid default AI looks**: purple-on-white / purple-indigo gradients; warm cream (#F4F1EA) + terracotta; broadsheet hairline / zero-radius newspaper cosplay; unearned dark mode; glow stacks; pill clusters; emoji ornament

## Frame (every page)

Readers name these first when a page looks wrong. Check them in screenshots:

- One clear **title on the first screen** (`h1`); every section has a heading
- **Equal outer margins**; no section huddled on one side with empty half-screen void
- Asymmetry inside the grid, never in the frame; a void only when something closes it
- No blank stretch taller than about half a viewport; section gaps ~120-240px desktop
- Headlines: two lines or fewer at every width

## Process

### 1. Ground in the subject

Name the product/subject, audience, and primary job of the page. If unclear,
propose one concrete reading and confirm.

**Inventory** eight to twelve things that belong to this client and not a
competitor (name meaning, place, materials, numbers, constraints, rituals,
printed artefacts). Distinctiveness comes from that list, not a generic
"premium SaaS" costume.

### 2. Write the argument

Before art direction, list the page as claims with proof (one line per section)
per `references/copy.md`. Delete sections with no claim. Avoid the stock
hero → logos → three features → testimonial → pricing → CTA sequence unless
the claims require it.

### 3. Deal a direction (no scripts)

Without upstream `draw.mjs`, invent **three** sharply different directions,
then pick one with the user (or state the pick if AFK).

Each direction must state:

- **Idea**: one sentence from the inventory (not "clean modern"). Competitor
  test: if swapping the nearest competitor still works, the idea is category
  fluff; rewrite.
- **Composition**: hero treatment + section rhythm (ASCII wireframe welcome)
- **Type**: one family or two clearly distinct families; roles for display/body
- **Palette**: 4-6 named hex values with jobs (ground, ink, accent, support…)
- **Imagery plan**: real photos, product UI crop, illustration, or none, and why
- **One live thing** (optional but strong): one visitor action or visit-varying
  detail made from the idea, with a no-script fallback

Prefer directions that would fail a "could this be any other brand?" test.

### 4. Review the plan against tells

Before coding, scrub the plan using `references/tells.md` and the hard rules.
If any axis looks like the default you would produce for any similar brief,
revise it and say what changed.

Also avoid: single-word headline accents, ALL-CAPS labels as chrome, unnecessary
eyebrows, identical card grids, soft grey shadow kits, gradient washes as
decoration, middle-dot meta strings, decorative `→` on every link.

### 5. Build

Implement against the locked plan. Prefer host design tokens when building
inside an existing app. Keep CSS specificity sane; don't let utility classes
fight element rules into a mess.

Order of emphasis: tokens → hero at desktop and phone → each section from its
blueprint with real content → imagery → live thing → fullness/frame → states
and semantics → motion last.

Write copy as design content: active voice, sentence case, same action name
through a flow, specific empty/error states. See `references/copy.md`.

Quality floor without announcing it: responsive to mobile, visible keyboard
focus, `prefers-reduced-motion` respected, usable contrast.

### 6. Critique loop

If browser/screenshot tools exist (Cursor browser / CDP), capture desktop and
mobile, then critique with `references/critique.md`. Fix the worst issues, look
again (at most three rounds). Without screenshots, still do a structured
self-critique against tells, hero budget, brand test, and frame rules.

Spend boldness in one place; remove one accessory before shipping the pass.

## Redesign, restyle, or review

When changing an existing page or app screen (retired standalone
`redesign-existing-projects` lives here):

1. **Record the before.** Run or open the current UI; screenshot desktop and
   mobile; note stack, styling method, and what must survive (routes, forms,
   data, behaviour, brand assets).
2. **A review stops here.** Critique with `references/critique.md`; list the
   three changes that would move the page most.
3. **Keep stack, content, and what works.** No drive-by framework migration.
   Restyle: keep layout; refresh type, colour, components. Redesign: new
   direction and section blueprints inside existing components/routes.
4. **Order of impact:** type → colour → frame → states → replace stock
   components (icon cards, pills, gradient blobs, identical card grids).
5. **Prove it.** After screenshots vs before; click through links, forms, and
   menus that worked before.

Pair with `polish` for a final micro-pass that must not smuggle a redesign.

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
| Scroll scenes | `references/scenes.md` |

When references mention upstream `inspect.mjs` / `draw.mjs` / `lint.mjs` /
`assets.mjs`, **do not expect those binaries**. Perform the same checks
manually or with available browser tools. Prefer Cursor browser tools over
installing Chrome DevTools MCP solely for this skill.

## Restraint

Removal of tells is not enough: replace them with substance (strong type, real
imagery, decisive colour fields, complete section content). An empty "clean"
page loses to a richer page that still has tells.

## License notes

Anthropic frontend-design portions: see `LICENSE-anthropic.txt`. Taste-skill /
`design-taste-frontend` reference material was snapshotted as static markdown
without its executable scripts, asset pipelines, or direction libraries.
