---
name: deslop
description: >-
  Remove AI-generated code slop and clean up code style on a branch or diff.
  Use when asked to deslop, clean AI code noise, strip unnecessary comments,
  or tidy a PR without changing behavior. Complements unslop (prose).
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
