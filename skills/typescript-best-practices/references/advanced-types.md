# Advanced types

Type-level design beyond the daily rules in `SKILL.md`: generics, conditional types,
mapped and template literal types, utility types, discriminated-union modeling, and
type tests. The `SKILL.md` rules (no `as`, brands via guards only) apply here too.

Use for type-safe libraries or shared utilities, complex inference or key remapping,
custom utility types, and type tests that lock intended inference.

## Core concepts

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
[discriminated-unions.md](discriminated-unions.md).

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
form typing): [advanced-type-patterns.md](advanced-type-patterns.md).
