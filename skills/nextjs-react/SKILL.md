---
name: nextjs-react
description: >-
  Next.js App Router and React TypeScript patterns: Server Components, client
  boundaries, data fetching, routing, and performance. Use when editing Next.js
  or React app code (.tsx pages/layouts/route handlers, hooks, client
  components). Pair with typescript-best-practices for typing rules; do not
  replace project UI libraries with unrelated component kits.
---

# Next.js and React (TypeScript)

Focus on React and Next.js App Router prescriptions. Respect the repository's
existing UI system, styling approach, and component library. Do not introduce
Shadcn, Radix, Tailwind, or other kits unless the project already uses them or
the user explicitly asks.

Pair with `typescript-best-practices`.

## Code style and structure

- Write concise TypeScript with clear names (`isLoading`, `hasError`, `canSubmit`)
- Prefer functions and composition over classes for UI logic
- Prefer iteration and small modules over duplication
- Typical file order: exports, subcomponents, helpers, static content, types

## Naming and modules

- Prefer kebab-case directories when that matches the repo
- Prefer named exports for components and hooks
- Reserve default exports for framework-required files (`page.tsx`, `layout.tsx`,
  `route.ts`, `loading.tsx`, `error.tsx`, config files)

## TypeScript usage

- Prefer `interface` for props and object shapes; `type` for unions and aliases
- Avoid enums; prefer const objects + derived unions
- Model UI state with discriminated unions when variants carry different data
- No type assertions; narrow or parse instead

## Next.js App Router

- Default to Server Components
- Add `'use client'` only for browser APIs, interactive state, or effects that
  cannot run on the server
- Keep client leaves small; pass serializable props from server parents
- Prefer framework data-fetching and caching patterns over ad-hoc client fetching
  for initial page data
- Use `loading.tsx` / `error.tsx` / `not-found.tsx` where the router supports them
- Wrap client-only trees in `Suspense` when streaming/fallback improves UX
- Use dynamic import for heavy optional client bundles
- Follow current Next.js docs for routing, fetching, and caching semantics

## React performance

- Minimize unnecessary `useEffect` and mirrored state
- Prefer deriving values during render when possible
- Optimize images with the platform's image component when the project uses it
  (explicit sizes, modern formats, lazy loading below the fold)

## Accessibility and UX

- Prefer semantic HTML and accessible names over div soup
- Match the project's existing layout and design tokens/components

## URL and client state

- Prefer the project's existing URL-state library or Next searchParams patterns
- Do not add a new URL-state dependency for a one-off


## App Router depth

For Server Components, streaming, parallel routes, caching, and advanced data-fetching patterns beyond the quick rules above, see:

- [app-router-patterns.md](references/app-router-patterns.md)
- [app-router-details.md](references/app-router-details.md)

Repository UI system and styling choices still win; do not introduce Tailwind or component kits unless the project already uses them or the user asks.

## State management

For choosing and applying client/server state libraries (Redux Toolkit, Zustand, Jotai, React Query) when the project already uses them or the user asks, see [state-management.md](references/state-management.md) and `references/state-*.md`. Prefer the repo's existing state approach; do not introduce a new library by default.

## Related skills

- `typescript-best-practices`, `vitest`
- `security-and-hardening` for auth/header/input reviews in Next route handlers
