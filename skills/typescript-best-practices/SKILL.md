---
name: typescript-best-practices
description: >-
  Daily TypeScript coding rules for .ts/.tsx work: discriminated unions, branded
  types via type guards (never assertions), unknown over any, schema-derived
  types, exhaustiveness, const assertions, and variable conventions. Use when
  reading or editing TypeScript. Pair with framework skills (React, Next.js,
  NestJS, Vitest) when the task is framework-specific.
---

# TypeScript Best Practices

Apply these rules when reading or editing TypeScript. Repository conventions and
config win when they conflict. Pair with framework skills when the work is in
React, Next.js, NestJS, Vitest, or similar.

## Type shape rules

| Rule | Summary |
|------|---------|
| Discriminated unions | Model variants with a shared literal discriminant (`kind` / `type` / `status`). No optional-field bags for mutually exclusive states. |
| Branded types | Brand primitives with `& { readonly __brand: "X" }`. Create brands only through verifying type guards or parsers that return a narrowed type. Never use `as` to mint a brand. |
| Constructive modeling | Prefer shapes where illegal values cannot be constructed (`[T, ...T[]]` for non-empty, start + duration for ranges). |
| Simplest total type | Keep `T[]` while operations stay total. Strengthen only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | Untrusted and external data is `unknown`. Narrow before use. |
| Schemas before guards | Prefer the repo's runtime schema library (`z.infer`, etc.) over hand-written property guards when validating external data. |
| No `as` casts | Do not use type assertions. Narrow with discriminants, `in`, `typeof`/`instanceof`, or honest type guards. Use `satisfies` to check values without widening. |
| Exhaustiveness | `const _exhaustive: never = x` in default arms so new variants fail at compile time. |
| Boundary validation | Parse at trust boundaries into named domain types. Trust types inside the boundary. |
| Schema-derived types | Prefer `Pick` / `Omit` / `Parameters` / `ReturnType` / `Awaited` / `typeof` before new interfaces. |
| Object args | Prefer object parameters over long positional lists, except hot paths. |

Examples: `references/patterns.md`.

## `interface` vs `type`

- Prefer `interface` for object shapes (props, records, public object APIs).
- Prefer `type` for unions, intersections, mapped/conditional types, and aliases.

## Variables and literals

- Prefer `const` and `as const` so literals stay narrow and structures stay readonly where that is intended.
- Prefer const objects + derived unions over enums:

```ts
const ROLES = ["admin", "user", "guest"] as const;
type Role = (typeof ROLES)[number];
```

- Prefer a literal union when only the value changes; prefer a discriminated union when each state needs different data.
- Prefer boolean names with auxiliary verbs (`isLoading`, `hasError`, `canEdit`).
- With `strictNullChecks`: use `null` for explicit empty; use `undefined` for omitted/optional absence. Stay consistent inside a module.

## Imports, async, and structure

- Prefer named exports. Reserve default exports for framework-required entry files.
- Prefer separate `import type` for type-only imports when the project already does.
- New IO should be async at boundaries (`fs/promises`, etc.). Avoid expanding sync call chains in new code.
- Avoid silencing errors with empty `.catch(() => fallback)`. Log or propagate failures.
- Prefer `@ts-expect-error` over `@ts-ignore` when a suppression is unavoidable and justified; document why. Prefer fixing the type instead.

## Runtime validation

- Define Zod (or the repo's schema lib) schemas as the source of truth; infer types with `z.infer<>`.
- Use `safeParse` for expected user/input failure; use `parse` at trust boundaries where invalid data is a bug.

## Testing and telemetry

- Prefer real tests over mocks when practical. Mock only what cannot run locally.
- Prefer structured logging over `console.log` in shipped code. Never log secrets.

## Modern JavaScript patterns (in TypeScript)

For async/await, iterators/generators, modules, and functional patterns that still apply under TypeScript, see [modern-js-patterns.md](references/modern-js-patterns.md) and `references/modern-js-*.md`. TypeScript typing rules in this skill win when they conflict with untyped JS examples.

## Related skills

- Complex generics / mapped / conditional types: `typescript-advanced-types`
- tsconfig, diagnostics, migration, monorepo compiler issues: `typescript-toolchain`
- Framework UI/routing: `nextjs-react` (and other framework skills)
- Tests: `vitest`
- Security audit: `security-and-hardening` (TypeScript references under that skill)
- API/docs generation: `typescript-docs`
