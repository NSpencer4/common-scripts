---
name: postgres
description: >-
  PostgreSQL schema design, indexing, query patterns, operations (pooling,
  replication, upgrades), table design, RLS-oriented patterns, SQL review, and
  advanced PG features. Use when writing SQL, designing schemas, optimizing
  queries, reviewing migrations, or debugging Postgres performance. For Drizzle
  ORM APIs use postgres-drizzle.
---

# PostgreSQL

Vendor-neutral Postgres guidance. Prefer the project's actual host, version, and migration tooling.

## Reference routing

| Need | Reference |
|------|-----------|
| Schema, types, FKs, normalization | [schema-design.md](references/schema-design.md), [table-design.md](references/table-design.md), [table-design-details.md](references/table-design-details.md) |
| Indexes | [indexing.md](references/indexing.md) |
| Query patterns / anti-patterns | [query-patterns.md](references/query-patterns.md), [query-optimization.md](references/query-optimization.md) |
| Transactions / isolation | [transaction-isolation.md](references/transaction-isolation.md) |
| Pooling / connections | [connection-pooling.md](references/connection-pooling.md) |
| Diagnostics | [performance-diagnostics.md](references/performance-diagnostics.md) |
| Security / roles | [security-roles.md](references/security-roles.md) |
| RLS and app patterns | [patterns-rls.md](references/patterns-rls.md) |
| SQL / PG review checklist | [code-review.md](references/code-review.md) |
| Advanced types/features | [advanced-features.md](references/advanced-features.md) |
| Backups / replication / upgrades | [backup-restore.md](references/backup-restore.md), [logical-replication.md](references/logical-replication.md), [hot-standby.md](references/hot-standby.md), [major-version-upgrades.md](references/major-version-upgrades.md) |
| Bulk load | [bulk-loading.md](references/bulk-loading.md) |
| SQL query tuning / EXPLAIN | [sql-optimization-patterns.md](references/sql-optimization-patterns.md), [sql-optimization-universal.md](references/sql-optimization-universal.md) |

## Related skills

- `postgres-drizzle` — Drizzle ORM schemas, relations, migrations
- `nestjs-best-practices` — Nest data-access rules when calling Postgres from Nest
- `api-design-principles` — API shape above the database
