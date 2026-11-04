# TypeScript / Node security review workflow

Use when the stack is TypeScript or Node (Express, NestJS, Next.js, and similar). Classify findings by severity with concrete remediation. Prefer framework-specific fixes that match the repository.

## Steps

1. **Scope** — Prioritize auth, authorization, data handling, public endpoints, and config. Search for sensitive patterns (`eval`, `exec`, `innerHTML`, password/JWT handling).
2. **Authn/authz** — JWT algorithms/expiry/claims, session cookies, password hashing (bcrypt/argon2), route guards/middleware coverage.
3. **Injection** — SQL/NoSQL, command (`exec`/`spawn`), template, and LDAP injection. Prefer parameterized queries / ORM binders.
4. **Input validation** — Boundary schemas (Zod or the repo's validator). No trust of client-only checks. See [input-validation.md](input-validation.md).
5. **XSS** — `dangerouslySetInnerHTML`, sanitization, CSP. See [xss-prevention.md](xss-prevention.md).
6. **Secrets** — Hardcoded credentials, committed `.env`, logging of secrets. Report locations only; do not echo secret values.
7. **Dependencies** — `pnpm`/`npm`/`yarn` audit as appropriate; assess exploitability, not just advisory presence. See [dependency-security.md](dependency-security.md).
8. **Headers & config** — Helmet or equivalents, CORS, rate limits, HTTPS, cookie flags. See [security-headers.md](security-headers.md).
9. **Report** — Structured findings; re-scan for the same pattern after Critical/High hits.

Also read [owasp-typescript.md](owasp-typescript.md) and [common-vulnerabilities.md](common-vulnerabilities.md).

## Example: JWT

```typescript
import jwt from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET || JWT_SECRET.length < 32) {
  throw new Error("JWT_SECRET must be set and at least 32 characters");
}

function generateToken(userId: string): string {
  return jwt.sign({ sub: userId }, JWT_SECRET, {
    algorithm: "HS256",
    expiresIn: "15m",
    issuer: "my-app",
    audience: "my-app-client",
  });
}

interface JwtPayload {
  sub: string;
}

function isJwtPayload(value: unknown): value is JwtPayload {
  if (typeof value !== "object" || value === null || !("sub" in value)) {
    return false;
  }
  const sub = Reflect.get(value, "sub");
  return typeof sub === "string";
}

function verifyToken(token: string): JwtPayload {
  const payload: unknown = jwt.verify(token, JWT_SECRET, {
    algorithms: ["HS256"],
    issuer: "my-app",
    audience: "my-app-client",
  });
  if (!isJwtPayload(payload)) {
    throw new Error("Unexpected JWT payload shape");
  }
  return payload;
}
```

Prefer a Zod schema for JWT claims when the project already uses Zod.

## Example: SQL

```typescript
// Bad: string concatenation
await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// Good: parameters
await db.query("SELECT id, name, email FROM users WHERE email = $1", [email]);
```

## Output format

1. Security posture summary
2. Critical
3. High
4. Medium
5. Low
6. Positive observations
7. Remediation roadmap with code-oriented fixes

## Constraints

- Not a substitute for professional pentesting
- Code-level focus; infrastructure is out of scope unless configured in-repo
- Do not print discovered secret values
- Keep recommendations proportional to risk
