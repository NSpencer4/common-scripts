---
name: atomic-presentational-ui
description: >-
  Build or review reusable, themeable UI components and Storybook catalogs using
  atomic design boundaries in this monorepo. Use when adding or refactoring shared
  or app UI, writing Storybook stories (including full-page stories), composing
  pages from primitives, or building a page/route from design.html, design.png,
  and a route document via sub-agents.
---

# Atomic presentational UI

Use this skill for reusable UI, Storybook documentation, page composition, and
design-to-page builds in the launch-sequence monorepo.

Pair with `frontend-design` for visual art direction on marketing/public surfaces.
This skill owns component boundaries, Storybook taxonomy, and the construction
workflow.

## Monorepo paths

- Shared primitives and SaaS compositions: `packages/shared/ui/components`
- Storybook: `packages/shared/ui/storybook`
- Domain apps: `packages/apps/<app>` (app-specific presentational sections stay here)

Keep domain rules, service integrations, and product-specific content with the
app that owns them. Put generally reusable presentational components in
`packages/shared/ui`.

## Structure

- Inspect existing shared components, theme tokens, and Storybook taxonomy before
  creating APIs. Reuse or extend existing primitives when their semantics fit.
- For every app UI task, inspect the shared UI library and Storybook before adding
  page markup. Route and page components should compose named components and layout
  primitives; keep raw semantic HTML inside those components rather than directly
  in page components.
- Make each page section an app-specific component when it carries domain content
  or presentation. Reuse or extend a generic shared component for cross-project
  patterns such as responsive layouts, cards, headings, and actions.
- Treat generic, reskinnable presentational components as the default. Build
  higher-order UI and page sections by composing those components.
- Give each reusable primitive a focused API and its own component module. Small
  elements such as buttons, badges, headlines, paragraphs, and form controls are
  components, not styling details hidden inside page-sized components.
- Compose larger patterns from these atoms. Prefer children slots and data-driven
  props. Avoid a single large component for a page or section when its parts can
  be independently reused and documented.
- Do not split markup into meaningless wrappers solely to increase component count.
  A component should express a reusable semantic or visual responsibility.
- Before adding a shared component, inspect the library for an equivalent. Keep
  project-specific workflows and integrations out of the generic library unless
  there is a stable, reusable contract.

## Themeability

- Style reusable components through host-provided semantic tokens for colors,
  typography, spacing, borders, and surfaces. Do not hard-code a particular
  project's palette or brand fonts into shared component styles.
- Keep component behavior independent from a specific app theme. Verify that the
  shared theme contract is documented and that host projects can map their tokens
  to it.
- Prefer explicit TypeScript unions for meaningful variants. Avoid permissive
  catch-all props and untyped boundaries. Follow repository TypeScript skills
  (`typescript-best-practices`): no type assertions; `interface` for object
  shapes; `type` for unions.

## Storybook organization and docs

Storybook should display the atomic reusable library and group each app's
domain-specific higher-order components in their own displays.

Use these titles:

- Chakra-style category titles for shared primitives: `Layout`, `Typography`,
  `Buttons`, `Date and Time`, `Forms`, `Collections`, `Overlays`, `Disclosure`,
  `Feedback`, `Data Display`, `Utilities`
- `SaaS/<Category>/…` for reusable software-product compositions
- `<App>/Presentational/<Group>` for app-specific higher-order components and
  section compositions

Give each form control its own entry under `Forms` (or `Date and Time` for
date/time pickers), including inputs, text areas, selects, checkboxes, radios,
phone/search controls, toggles, and range controls when present.

For every reusable component, provide a dedicated Storybook entry with:

- A concise purpose description
- Controls for meaningful props and explicit variant options
- Named stories for each meaningful variant
- Relevant states (disabled, error, success, selected, empty, responsive) where
  supported

A rendered example alone is insufficient. Use component descriptions or autodocs
so API intent is visible in Docs as well as Controls.

Example composition: `SectionContainer` (`Layout`) with `Headline` / `Paragraph`
(`Typography`), `MediaCard` (`Data Display`), `TextInput` (`Forms`), `Button`
(`Buttons`). The host app supplies theme tokens and owns domain-specific sections.

### Page stories

Every app page or route must have a full-page Storybook story so the components
that make up the page are visible together.

- One stories file per route under
  `packages/shared/ui/storybook/src/stories/<app>/pages/`
- Title: `<App>/Pages/<Page Name>` with a `FullPage` story and
  `layout: 'fullscreen'`
- Render the real route component from the app (not a copy of its markup) inside
  the app's theme provider so the story cannot drift from the page
- Docs description states the route path and lists, in page order, every component
  the page uses with its Storybook title (including shared components such as
  `StatTile` or `DataTable`)
- Create the page story when creating a page; update it in the same change when a
  page gains, loses, or reorders components or changes its route
- Treat a page without a current page story as incomplete
- Verify the page story renders in the built Storybook before reporting the page
  done

## Component workflow

1. Map the requested UI to existing shared atoms, compositions, layouts, and
   app-specific patterns.
2. Define the smallest useful shared API and explicit variants before implementing
   compositions.
3. Implement shared components with semantic tokens, accessible native semantics,
   and typed content slots.
4. Compose app-specific components from the shared primitives; avoid duplicating
   their behavior or visual rules.
5. Add or update individual Storybook docs in the correct group, showing all
   meaningful variants and states.
6. Add or update the page's full-page story when the page composition changes.
7. Update the shared UI README when public exports or the theme contract change.
8. Run typecheck, lint, and relevant builds as required by repository validation
   (`pnpm run check.all` before calling a task complete). Report checks that could
   not run and known gaps.

Keep integration-specific behavior local unless there is a stable, reusable
contract. For example, a vendor-backed address lookup should not be represented as
a generic text field unless its lookup behavior is actually implemented and
configurable.

## Building pages from designs and documentation

When asked to build a page or route from supplied designs (for example
`design.html`, `design.png`) and a route document, always build it with sub-agents
in this order. Do **not** build the components yourself in the main session.

1. Read the route document and design first, then inspect the shared UI library,
   the target app, and Storybook. Create a working branch if on the default branch.
2. Inventory the components the page needs and split them into:
   - Reusable SaaS or generic components for
     `packages/shared/ui/components/src/components/saas/` (stories under
     `SaaS/<Category>/…`) and shared primitives (Chakra category titles such as
     `Layout`, `Forms`, `Data Display`)
   - App-specific sections for the owning app (stories under
     `<App>/Presentational/<Group>`)
   Reuse existing components before adding new ones.
3. You are the manager of these sub-agents and accountable for the result. Spawn
   one low-effort, cheap sub-agent (Haiku, low effort) per component, in parallel.
   Give each a self-contained brief with:
   - The exact props API
   - The exact files it may create (component, CSS, and Storybook story)
   - The conventions to copy
   - The rule to edit nothing else
   Judge each agent's output against your own standard. If it is sub-par, send it
   back to the same agent with specific, actionable corrections until the result is
   acceptable. Build shared components first, then app sections that compose them.
4. Each component gets its own file and its own Storybook entry with a purpose
   description, controls, and a named story for every meaningful variant and state.
5. Wire exports, CSS imports, the route, and the router yourself after the agents
   finish, since those shared files would otherwise conflict.
6. Review the agents' output rather than trusting their reports: run typecheck,
   lint, and the build; build Storybook; check the page in a browser at desktop and
   mobile widths against the design. Wherever the result falls short, return it to
   the responsible sub-agent with specific corrections until it passes.
7. Add or update the page's full-page Storybook story listing every component on
   the page, and confirm it renders in the built Storybook.
8. Update the shared UI README when public exports change. Report gaps between the
   design and the route document instead of silently filling them.
