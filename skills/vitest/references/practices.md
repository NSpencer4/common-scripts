# Vitest practice notes (merged)

Project-oriented patterns retained from the prior Vitest skill install.

# Vitest

Prefer Vitest for unit and component tests in this environment. Prefer the
project's existing Vitest config and scripts over ad-hoc runners.

## Test structure

- Name files `*.test.ts`, `*.test.tsx`, `*.spec.ts`, or `*.spec.tsx` to match the repo
- Colocate tests with source or follow the repo's `__tests__` / `tests` convention
- Use descriptive `it`/`test` names that state expected behavior
- Nest with `describe` for related cases
- Pattern: `describe('Unit', () => { it('should …', () => {}) })`

## Effective mocking

- Mock external boundaries (network, DB, time) to keep unit tests focused
- Use `vi.mock()` for module mocks
- Use `vi.spyOn()` for specific functions/methods
- Use `mockImplementation` / `mockReturnValue` / `mockResolvedValue` as needed
- Reset or restore between tests: `vi.clearAllMocks()`, `vi.restoreAllMocks()`, or config `restoreMocks`
- Prefer real implementations when cheap and deterministic (see typescript-best-practices)

## Async tests

- Use `async`/`await` and Vitest async matchers (`resolves` / `rejects`)
- Avoid dangling promises; always await expectations
- For fake timers: `vi.useFakeTimers()` / `vi.useRealTimers()` with explicit advances

## Snapshots

- Use sparingly for stable, intentional serializations
- Prefer focused assertions for behavior
- Review snapshot diffs carefully before accepting

## React components

- Prefer Testing Library (`@testing-library/react`) over Enzyme-style tests
- Assert user-visible behavior and accessibility roles/labels/text
- Prefer `userEvent` over low-level `fireEvent` when available

## Common matchers

- Equality: `toBe`, `toEqual`, `toStrictEqual`
- Truthiness: `toBeTruthy`, `toBeFalsy`, `toBeNull`, `toBeUndefined`, `toBeDefined`
- Numbers: `toBeGreaterThan`, `toBeLessThanOrEqual`, …
- Strings/collections: `toMatch`, `toContain`, `toHaveLength`
- Objects: `toHaveProperty`, `toMatchObject`
- Errors: `toThrow`
- Mocks: `toHaveBeenCalled`, `toHaveBeenCalledWith`, `toHaveBeenCalledTimes`

## TypeScript

- Type test data with the same domain types as production code
- Prefer `unknown` for untyped fixtures until narrowed
- Do not use type assertions to force mock shapes; build valid fixtures or use
  schema parsers
