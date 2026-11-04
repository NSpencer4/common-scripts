---
name: typescript-docs
description: >-
  TypeScript API documentation with JSDoc, TypeDoc, and framework-oriented
  examples. Use when generating or improving public TypeScript API docs for
  NestJS, Express, React, and similar stacks. For Architecture Decision Records,
  use architecture-decision-records. For prose AI-tell cleanup, use unslop.
---

# TypeScript Documentation

Produce documentation that matches the repository's audience: inline JSDoc for
editors and generated API references when the project uses TypeDoc (or equivalent).
For significant architectural decisions, use `architecture-decision-records`
(this skill may still cite ADR-oriented TypeScript examples in references).

## When to use

- Public API / package documentation
- Framework-facing examples (NestJS controllers, React hooks, Express routes)
- Doc validation / CI doc generation setup
- Not primary owner of ADRs (use `architecture-decision-records`)

## Quick reference

| Tool | Purpose |
|------|---------|
| TypeDoc | API reference generation from TS + JSDoc |
| JSDoc tags | Inline contracts (`@param`, `@returns`, `@throws`, `@example`, `@remarks`, `@see`, `@deprecated`) |
| ADR markdown | Record architectural choices |

Prefer the package manager and doc scripts already in the repo. Do not add
TypeDoc or CI pipelines unless asked or the task is explicitly to set them up.

## Workflow

1. Identify the public surface (exports, modules, frameworks in use).
2. Document exported functions, classes, types, and non-obvious invariants.
3. Add `@example` blocks that compile against real types (no fake APIs).
4. For design choices that bind the team, add or update an ADR.
5. If the repo already generates docs, run the existing script and fix failures.

### JSDoc example

```typescript
/**
 * Authenticates a user and returns access tokens.
 *
 * @param credentials - User login credentials
 * @returns Authentication result with tokens
 * @throws {InvalidCredentialsError} If credentials are invalid
 * @example
 * ```typescript
 * const result = await authService.login({ email, password });
 * ```
 */
async function login(credentials: LoginCredentials): Promise<AuthResult> {
  // ...
}
```

### ADR skeleton

```markdown
# ADR-001: Title

## Status
Proposed | Accepted | Superseded

## Context
Why a decision is needed.

## Decision
What we chose.

## Consequences
What becomes easier or harder.
```

## Best practices

- Document exported APIs; skip obvious private helpers unless behavior is subtle
- Keep examples short and type-correct
- Never put secrets or production credentials in docs or examples
- Prefer linking to canonical docs over duplicating framework tutorials
- Match existing doc tone and file layout in the repository

## Constraints

- Do not invent a parallel documentation system when one exists
- Do not install doc tooling unless the task requires it
- Framework patterns: see `references/framework-patterns.md` and `references/examples.md`
- TypeDoc options: `references/typedoc-configuration.md`
- JSDoc detail: `references/jsdoc-patterns.md`
- ADR patterns: `references/adr-patterns.md`
- CI sketch: `references/pipeline-setup.md`
- Validation notes: `references/validation.md`

## Related skills

- `typescript-best-practices` for typing rules in examples
- `security-and-hardening` when documenting security-sensitive APIs
- `architecture-decision-records` for ADR authoring
