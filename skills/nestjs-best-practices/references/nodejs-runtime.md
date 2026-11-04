# Node.js runtime notes (merged into Nest skill)

Framework-agnostic Node.js backend habits useful alongside Nest. **Do not switch a Nest app to Express/Fastify because of this file.** For HTTP surface, modules, and DI, follow Nest + project AGENTS rules.

## Always-on practices

- TypeScript at trust boundaries; validate input (Zod/Joi/class-validator as the project already does)
- No hardcoded secrets; config from env
- Structured logging; correlate request IDs when the platform provides them
- Rate limiting and CORS with explicit origins in production
- Connection pooling for databases
- Health checks for orchestration
- Graceful shutdown: stop accepting work, drain in-flight requests, close pools
- Prefer dependency injection (Nest DI tokens) over service locators

## Error handling

- Distinguish operational errors from programmer bugs
- Map domain failures to typed HTTP errors at the edge (Nest filters/exceptions)
- Never swallow async errors; reject or log+rethrow with context
- Avoid leaking stack traces to clients

## Data access (ORM-agnostic)

- Keep transactions on one connection/handle for the whole unit of work
- Avoid N+1; batch or join deliberately
- Index foreign-key and filter columns you actually query
- Migrations for every schema change

## Caching

- Cache read-heavy, infrequently changing data behind clear TTLs and keys
- Invalidate on write paths you own; do not invent cache layers for every endpoint
- Treat cache as optional acceleration, not source of truth

## Auth (conceptual)

- Verify tokens/sessions at the edge (guards); authorize in the domain
- Short-lived access credentials; rotate secrets
- Do not log tokens or passwords

## When Express/Fastify patterns appear in upstream material

Ignore framework-specific middleware stacks unless you are explicitly building a non-Nest Node service. Nest pipes, guards, interceptors, and filters are the counterparts.
