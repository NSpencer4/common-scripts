# Snapshot provenance

Merged static skill (not installed via `npx skills`). Do not auto-update.

## Sources (2026-11-04)

- https://www.skills.sh/wshobson/agents/typescript-advanced-types
- https://www.skills.sh/jeffallan/claude-skills/typescript-pro (type-system portions; assertion-based brand factories removed)
- https://www.skills.sh/sickn33/agentic-awesome-skills/typescript-expert (type-level portions only)
- https://www.skills.sh/mkosir/typescript-style-guide/typescript-discriminated-unions

## Conflict resolutions applied

- No type assertions; brands via guards/parsers only
- `interface` for objects; `type` for unions and advanced aliases
