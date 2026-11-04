# Error playbook (quick)

Use after reading the full diagnostic text and the surrounding code.

| Symptom | Likely cause | Direction |
|---------|--------------|-----------|
| `TS2307` Cannot find module | Wrong resolution mode, missing export, path mapping, or package `exports` | Confirm `moduleResolution`, package entrypoints, and whether types exist |
| `TS2322` / `TS2345` assignability | Real shape mismatch, optional/exactOptional mismatch, readonly variance | Fix the data model; avoid assertions |
| `TS2339` property does not exist | Missing narrowing, wrong discriminant, incomplete props | Narrow first; widen types only with evidence |
| `TS18046` / `unknown` | Unchecked `unknown` | Narrow or parse with a schema |
| `TS7053` / index access | `noUncheckedIndexedAccess` | Handle `undefined` or use a verified non-empty structure |
| `TS2589` / instantiation depth | Over-recursive conditional types | Bound recursion; simplify utilities |
| Extremely slow checks | Massive unions, circular generics, too-broad includes | Measure with extended diagnostics; split programs |

Prefer fixing the contract over suppressing the error.
