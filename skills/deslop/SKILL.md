---
name: deslop
description: >-
  Remove AI-generated code slop on a branch or diff without changing behavior.
  Use when asked to deslop, clean AI code noise, strip unnecessary AI comments,
  or tidy a PR's AI tells in code. Do not use for general clarity refactors
  (code-simplification) or prose AI-tell cleanup (unslop).
---

# Remove AI code slop

Check the diff against the repo default branch (or a fixed point the user names) and remove AI-generated slop introduced in the change.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged unless fixing a clear bug.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences).
