---
name: typescript-advanced-types
description: >-
  Advanced TypeScript type-system patterns: generics with constraints, conditional
  types and infer, mapped types, template literal types, utility types, branded
  types via guards, and discriminated unions. Use when implementing complex type
  logic, reusable type utilities, type-safe APIs, or exhaustiveness-safe state
  models. Pair with typescript-best-practices for daily rules.
---

# TypeScript Advanced Types

Guidance for generics, conditional types, mapped types, template literal types,
utility types, and discriminated-union modeling. Daily coding rules live in
`typescript-best-practices`; this skill goes deeper on type-level design.

**Hard rule:** do not use type assertions (`as`). Brand and narrow only through
type guards, parsers, and control-flow narrowing. Prefer `satisfies` when checking
that a value matches a type without widening.

Prefer `interface` for object shapes and `type` for unions, intersections, and
mapped/conditional aliases.

## When to use

- Building type-safe libraries or shared utilities
- Complex inference, key remapping, or template-literal APIs
- Discriminated unions for application state, props, or API results
- Custom utility types beyond the built-ins
- Type tests that lock intended inference

## Core concepts (summary)

### Generics

```ts
function identity<T>(value: T): T {
  return value;
}

interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(item: T): T {
  console.log(item.length);
  return item;
}
```

### Conditional types and `infer`

```ts
type IsString<T> = T extends string ? true : false;

type MyReturnType<T> = T extends (...args: never[]) => infer R ? R : never;
```

Prefer `never[]` (or precise parameter tuples) over loose parameter typing when
reimplementing inference helpers.

### Mapped types

```ts
type ReadonlyProps<T> = {
  readonly [P in keyof T]: T[P];
};

type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

### Template literal types

```ts
type EventName = "click" | "focus" | "blur";
type EventHandler = `on${Capitalize<EventName>}`;
```

### Built-in utilities

`Partial`, `Required`, `Readonly`, `Pick`, `Omit`, `Exclude`, `Extract`,
`NonNullable`, `Record`, `ReturnType`, `Parameters`, `Awaited`.

Reach for these (and `typeof`) before inventing a parallel helper.

## Discriminated unions

Use when variants are mutually exclusive and each variant needs different data.
Keep properties optional only when absence is independent of variant.

```ts
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function label<T>(state: RequestState<T>): string {
  switch (state.status) {
    case "idle":
      return "idle";
    case "loading":
      return "loading";
    case "success":
      return `ok:${state.data}`;
    case "error":
      return state.error.message;
    default: {
      const _exhaustive: never = state;
      return _exhaustive;
    }
  }
}
```

Prefer a shared literal discriminant (`status` / `kind` / `type`). Do not model
mutually exclusive states as independent booleans plus optionals.

Deep examples (props, function args, required vs optional fields):
`references/discriminated-unions.md`.

## Branded types (guards only)

```ts
type UserId = string & { readonly __brand: "UserId" };

function isUserId(input: string): input is UserId {
  return /^[0-9a-f-]{36}$/i.test(input);
}

function parseUserId(input: string): UserId {
  if (!isUserId(input)) {
    throw new Error(`Invalid user id: ${input}`);
  }
  return input;
}
```

Never write `input as UserId`. Validation belongs in the guard/parser.

## Type testing

```ts
type AssertEqual<T, U> = [T] extends [U] ? ([U] extends [T] ? true : false) : false;

type _ExpectString = AssertEqual<string, string>;
```

Failing assignments to `never` helpers also work as compile-time tests.

## Best practices

1. Prefer `unknown` over `any`
2. Prefer inference; annotate public APIs and tricky boundaries
3. Keep recursive conditional types bounded; watch compile time
4. Document non-obvious type utilities with short JSDoc
5. Enable strict compiler options when adding or hardening configs (see `typescript-toolchain`)

## Detailed patterns

Worked examples (event emitters, API clients, builders, deep readonly/partial,
form typing): `references/patterns.md`.
