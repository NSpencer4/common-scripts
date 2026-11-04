# common-scripts

Shared global agent instructions and skills, revision-controlled and linked into local AI tools.

## Layout

- `AGENTS.md` — canonical global instructions (Claude, Codex, OpenCode, Junie)
- `cursor/rules/global.mdc` — same instructions with Cursor frontmatter (`alwaysApply`)
- `skills/` — personal/global Agent Skills shared across tools
- `scripts/link-ai-globals.sh` — idempotent symlink installer for a new machine

## Link on this machine / a new device

```bash
git clone git@github.com:NSpencer4/common-scripts.git ~/WebstormProjects/common-scripts
~/WebstormProjects/common-scripts/scripts/link-ai-globals.sh
```

The script replaces existing skill dirs / instruction files with symlinks to this repo (after copying them into a timestamped backup under `~/.ai-globals-backup-*`).

Linked paths:

| Path | Target |
|------|--------|
| `~/.cursor/skills` | `skills/` |
| `~/.claude/skills` | `skills/` |
| `~/.codex/skills` | `skills/` |
| `~/.config/opencode/skills` | `skills/` |
| `~/.junie/skills` | `skills/` |
| `~/.claude/AGENTS.md` | `AGENTS.md` |
| `~/.claude/CLAUDE.md` | `AGENTS.md` (relative) |
| `~/.codex/AGENTS.md` | `AGENTS.md` |
| `~/.config/opencode/AGENTS.md` | `AGENTS.md` |
| `~/.junie/AGENTS.md` | `AGENTS.md` |
| `~/.cursor/rules/global.mdc` | `cursor/rules/global.mdc` |

Cursor built-in `~/.cursor/skills-cursor` is left alone.

## Editing

Edit files in this repo, then commit/push. Every linked tool picks up the change immediately through the symlinks.

## Skills catalog

109 skills with local `SKILL.md` content under `skills/`.
 Plus 19 symlink stubs whose targets are missing in this checkout (listed at the bottom).

Agents auto-match on the skill `description` unless marked **slash-only** (`disable-model-invocation: true`). Slash-only skills load only when you invoke them by slash command or skill name.

| Mode | Meaning |
|------|---------|
| auto | Model may load the skill when the conversation matches its description |
| slash-only | Only when you explicitly invoke it (slash command or skill name) |

Columns: **Skill** (dir under `skills/`), **Purpose**, **Activates when** (cues from the description), **Command** (documented slash invoke, if any), **Mode**.

### Process & reasoning

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`architect`](skills/architect/SKILL.md) | Sketch types, signatures, and module structure before code, then stay in the loop while implementation… | Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape | `/architect` | slash-only |
| [`architecture-decision-records`](skills/architecture-decision-records/SKILL.md) | Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision… | Use when documenting significant technical decisions, reviewing past architectural choices, or establishing decision processes | — | auto |
| [`architecture-patterns`](skills/architecture-patterns/SKILL.md) | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and… | Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use this… | — | auto |
| [`brainstorming`](skills/brainstorming/SKILL.md) | Explore unclear product or design intent before building | When the user asks to brainstorm, shape a design, or clarify what to build | — | auto |
| [`codebase-design`](skills/codebase-design/SKILL.md) | Shared vocabulary for designing deep modules | Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more… | — | auto |
| [`constraint-driven-development`](skills/constraint-driven-development/SKILL.md) | Establishes a project's quality bar as a written contract and stops agents quietly lowering it.… | Use when no quality bar is written down, when the user says "set up constraints" or "define our standards", when the user wants dimensions they… | — | auto |
| [`create-specification`](skills/create-specification/SKILL.md) | Create a new specification file for the solution, optimized for Generative AI consumption | Create a new specification file for the solution, optimized for Generative AI consumption. | — | auto |
| [`design-doc-mermaid`](skills/design-doc-mermaid/SKILL.md) | Create Mermaid diagrams (flowchart, sequence, class, ER, state, C4, architecture) from text or source… | Use when asked to create a diagram, generate mermaid, document architecture, or convert code to diagram | — | auto |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | Build and sharpen a project's domain model | Use when discussing codebase terminology, writing or editing a GLOSSARY | — | auto |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | Subjects non-trivial decisions to a fresh-context adversarial review before they stand | Use when stress-testing a plan, working in unfamiliar code, stakes are high (auth, security, migration, irreversible ops), or a confident output… | — | auto |
| [`excalidraw-diagram-generator`](skills/excalidraw-diagram-generator/SKILL.md) | Generate Excalidraw diagrams from natural language descriptions | Use when asked to "create a diagram", "make a flowchart", "visualize a process", "draw a system architecture", "create a mind map", or "generate… | — | auto |
| [`grill-me`](skills/grill-me/SKILL.md) | A relentless interview to sharpen a plan or design | Manual only (`/grill-me`). Not auto-matched from conversation. | `/grill-me` | slash-only |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md) | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go | Manual only (`/grill-with-docs`). Not auto-matched from conversation. | `/grill-with-docs` | slash-only |
| [`grilling`](skills/grilling/SKILL.md) | Grill the user relentlessly about a plan, decision, or idea until shared understanding | Use when the ask is underspecified, when the user wants to stress-test thinking, or uses grill/interview triggers ("grill me", "interview me",… | — | auto |
| [`how`](skills/how/SKILL.md) | "how does X work", code walkthroughs before changing something, and placement / ownership / layering… | Manual only (`/how`). Not auto-matched from conversation. | `/how` | slash-only |
| [`i-have-adhd`](skills/i-have-adhd/SKILL.md) | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state… | Invoke with /i-have-adhd; stays on until "stop adhd mode" | `/i-have-adhd` | slash-only |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through… | Manual only (`/improve-codebase-architecture`). Not auto-matched from conversation. | `/improve-codebase-architecture` | slash-only |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | Delivers changes in thin, verifiable slices, and breaks oversized work into ordered tasks with… | Use when implementing multi-file changes, picking up the next task from a plan, writing a plan from a spec, rolling out behind a feature flag,… | — | auto |
| [`prd`](skills/prd/SKILL.md) | Generate high-quality Product Requirements Documents (PRDs) for software systems and AI-powered features | Generate high-quality Product Requirements Documents (PRDs) for software systems and AI-powered features. Includes executive summaries,… | — | auto |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | Ground framework-specific decisions in official documentation for the installed versions | Use when correctness depends on a framework/library API or recommended pattern, when building boilerplate that will be copied, or when the user… | — | auto |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Drives development with the red-green-refactor loop | Use when implementing new logic or behavior, fixing bugs (prove-it with a failing test first), or changing existing behavior in a maintained… | — | auto |
| [`why`](skills/why/SKILL.md) | 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or… | Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds | `/why` | slash-only |

### Code quality & review

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`blast-radius`](skills/blast-radius/SKILL.md) | Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact… | Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust | `/blast-radius` | slash-only |
| [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md) | Automates CI/CD pipeline setup | Use when setting up or modifying build and deployment pipelines | — | auto |
| [`code-review`](skills/code-review/SKILL.md) | Review changes since a fixed point (commit, branch, tag, or merge-base) on two axes: Standards (repo… | Use when reviewing a branch, a PR, WIP changes, or "review since X" | — | auto |
| [`code-simplification`](skills/code-simplification/SKILL.md) | Simplifies code for clarity | Use when refactoring code for clarity without changing behavior | — | auto |
| [`cost-optimization`](skills/cost-optimization/SKILL.md) | Optimize cloud costs across AWS, Azure, GCP, and OCI through resource rightsizing, tagging strategies,… | Use when reducing cloud expenses, analyzing infrastructure costs, or implementing cost governance policies | — | auto |
| [`debugging-strategies`](skills/debugging-strategies/SKILL.md) | Master systematic debugging techniques, profiling tools, and root cause analysis to efficiently track… | Use when investigating bugs, performance issues, or unexpected behavior | — | auto |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | Manages deprecation and migration | Use when removing old systems, APIs, or features | — | auto |
| [`deslop`](skills/deslop/SKILL.md) | Remove AI-generated code slop and clean up code style on a branch or diff | Use when asked to deslop, clean AI code noise, strip unnecessary comments, or tidy a PR without changing behavior | — | auto |
| [`git-commit`](skills/git-commit/SKILL.md) | Making a Git commit or splitting changes into more than one commit | When the user asks to commit or types /commit, or when standing global/project Git instructions approve committing after validation | `/commit` | auto |
| [`make-pr-easy-to-review`](skills/make-pr-easy-to-review/SKILL.md) | Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer… | Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code… | — | auto |
| [`observability-and-instrumentation`](skills/observability-and-instrumentation/SKILL.md) | Instruments code so production behavior is visible and diagnosable | Use when adding logging, metrics, tracing, or alerting | — | auto |
| [`security-and-hardening`](skills/security-and-hardening/SKILL.md) | Hardens code against vulnerabilities | Use when auditing an input handler for vulnerabilities, when handling user input, authentication, data storage, or external integrations, or… | — | auto |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | Prepares engineering production deploys | Use when preparing to deploy to production, needing a pre-launch checklist, staged rollout, monitoring, or rollback plan | — | auto |
| [`technical-writing`](skills/technical-writing/SKILL.md) | Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE… | Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages | `/technical-writing` | slash-only |
| [`thermo-nuclear-code-quality-review`](skills/thermo-nuclear-code-quality-review/SKILL.md) | Run an extremely strict maintainability review for abstraction quality, giant files, and… | Manual only (`/thermo-nuclear-code-quality-review`). Not auto-matched from conversation. | `/thermo-nuclear-code-quality-review` | slash-only |
| [`typescript-security-review`](skills/typescript-security-review/SKILL.md) | Security review for TypeScript/Node.js apps: XSS, injection, CSRF, JWT/OAuth flaws, dependency CVEs, and… | Security review for TypeScript/Node.js apps: XSS, injection, CSRF, JWT/OAuth flaws, dependency CVEs, and secrets exposure. Use for… | — | auto |
| [`unslop`](skills/unslop/SKILL.md) | Cut AI tells from any writing | Manual only (`/unslop`). Not auto-matched from conversation. | `/unslop` | slash-only |

### Frontend & design

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`accessibility`](skills/accessibility/SKILL.md) | Audit and improve web accessibility following WCAG 2.2 guidelines | Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen reader support", "keyboard navigation", or "make accessible" | — | auto |
| [`atomic-presentational-ui`](skills/atomic-presentational-ui/SKILL.md) | Build or review reusable, themeable UI components and Storybook catalogs using atomic design boundaries… | Use when adding or refactoring shared or app UI, writing Storybook stories (including full-page stories), composing pages from primitives, or… | — | auto |
| [`browser-testing-with-devtools`](skills/browser-testing-with-devtools/SKILL.md) | Verifies UI in a real browser with Cursor browser / CDP tools | Use when building or debugging anything that renders in a browser, inspecting the DOM, capturing console errors, analyzing network requests,… | — | auto |
| [`frontend-design`](skills/frontend-design/SKILL.md) | Distinctive, intentional frontend visual design for new or reshaped UI. Combines anti-slop art… | Use when building, redesigning, polishing, or reviewing landing pages, marketing surfaces, product pages, heroes, or public-facing web UI, or… | — | auto |
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | Production-quality accessible responsive UI engineering (WCAG, state, loading, responsive) | Use when building or modifying interfaces with engineering depth | — | auto |
| [`image-to-code`](skills/image-to-code/SKILL.md) | Opt-in image-first website design: generate design image(s), analyze them, then implement. Use ONLY when… | Opt-in image-first website design: generate design image(s), analyze them, then implement. Use ONLY when the user explicitly asks for… | — | auto |
| [`modern-web-guidance`](skills/modern-web-guidance/SKILL.md) | Search tool for modern web development best practices | Search tool for modern web development best practices. MANDATORY: Execute FIRST for all HTML/CSS and clientside JS tasks. Do NOT skip —… | — | auto |
| [`polish`](skills/polish/SKILL.md) | Final quality pass for alignment, spacing, consistency, states, and micro-detail before shipping | Use when the user mentions polish, finishing touches, pre-launch review, something looks off, UI micro-detail (radius, shadows, icons, motion),… | — | auto |
| [`prototype`](skills/prototype/SKILL.md) | Build a throwaway prototype to answer a design question | Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like | — | auto |
| [`tailwind-design-system`](skills/tailwind-design-system/SKILL.md) | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive… | Use when creating component libraries, implementing design systems, or standardizing UI patterns | — | auto |
| [`web-perf`](skills/web-perf/SKILL.md) | Audit, diagnose, or optimize loading and interaction performance | Use when measure-first profiling points at frontend, backend, or query bottlenecks | — | auto |

### Platform & backend

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`api-design-principles`](skills/api-design-principles/SKILL.md) | Master REST and GraphQL API design principles to build intuitive, scalable, and maintainable APIs that… | Use when designing new APIs, reviewing API specifications, or establishing API design standards | — | auto |
| [`cf-cli`](skills/cf-cli/SKILL.md) | Cloudflare's official cf CLI (beta) for the public Cloudflare API and Workers projects | Cloudflare's official cf CLI (beta) for the public Cloudflare API and Workers projects. Use for finding and running Cloudflare commands… | — | auto |
| [`chrome-extensions`](skills/chrome-extensions/SKILL.md) | Build and publish Chrome Extensions using Manifest V3 best practices | Phrases like: 'Chrome extension'; 'browser extension'; 'manifest.json' | — | auto |
| [`cloudflare`](skills/cloudflare/SKILL.md) | Discover and choose Cloudflare products for apps, APIs, AI agents, storage, networking, and security | Discover and choose Cloudflare products for apps, APIs, AI agents, storage, networking, and security. Use for architecture and product… | — | auto |
| [`cloudflare-email-service`](skills/cloudflare-email-service/SKILL.md) | Implement or troubleshoot Cloudflare Email Sending and Email Routing integrations and their delivery… | Implement or troubleshoot Cloudflare Email Sending and Email Routing integrations and their delivery configuration. | — | auto |
| [`durable-objects`](skills/durable-objects/SKILL.md) | Build, debug, or review Cloudflare Durable Objects code for persistent state and coordination | Build, debug, or review Cloudflare Durable Objects code for persistent state and coordination. | — | auto |
| [`microservices-patterns`](skills/microservices-patterns/SKILL.md) | Design microservices architectures with service boundaries, event-driven communication, and resilience… | Use when building distributed systems, decomposing monoliths, or implementing microservices | — | auto |
| [`multi-stage-dockerfile`](skills/multi-stage-dockerfile/SKILL.md) | Create optimized multi-stage Dockerfiles for any language or framework | Create optimized multi-stage Dockerfiles for any language or framework | — | auto |
| [`nestjs-best-practices`](skills/nestjs-best-practices/SKILL.md) | NestJS best practices and architecture patterns for building production-ready applications | NestJS best practices and architecture patterns for building production-ready applications. This skill should be used when writing,… | — | auto |
| [`nextjs-on-cloudflare`](skills/nextjs-on-cloudflare/SKILL.md) | Build, migrate, and deploy Next.js apps on Cloudflare Workers with vinext | Use when starting a Next | — | auto |
| [`nextjs-react`](skills/nextjs-react/SKILL.md) | Next.js App Router and React TypeScript patterns: Server Components, client boundaries, data fetching,… | Use when editing Next | — | auto |
| [`postgres`](skills/postgres/SKILL.md) | PostgreSQL schema design, indexing, query patterns, operations (pooling, replication, upgrades), table… | Use when writing SQL, designing schemas, optimizing queries, reviewing migrations, or debugging Postgres performance | — | auto |
| [`postgres-drizzle`](skills/postgres-drizzle/SKILL.md) | Write or review PostgreSQL schemas, queries, migrations, and Drizzle ORM code | Write or review PostgreSQL schemas, queries, migrations, and Drizzle ORM code. Use for Postgres/Drizzle relations, indexing, pooling, or… | — | auto |
| [`rag-implementation`](skills/rag-implementation/SKILL.md) | Build Retrieval-Augmented Generation (RAG) systems for LLM applications with vector databases and… | Use when implementing knowledge-grounded AI, building document Q&A systems, or integrating LLMs with external knowledge bases | — | auto |
| [`typescript-advanced-types`](skills/typescript-advanced-types/SKILL.md) | Advanced TypeScript type-system patterns: generics with constraints, conditional types and infer, mapped… | Use when implementing complex type logic, reusable type utilities, type-safe APIs, or exhaustiveness-safe state models | — | auto |
| [`typescript-best-practices`](skills/typescript-best-practices/SKILL.md) | Daily TypeScript coding rules for .ts/.tsx work: discriminated unions, branded types via type guards… | Use when reading or editing TypeScript | — | auto |
| [`typescript-docs`](skills/typescript-docs/SKILL.md) | TypeScript documentation with JSDoc, TypeDoc, ADRs, and framework-oriented examples | Use when generating API docs, architecture decision records, or improving public TypeScript API documentation for NestJS, Express, React, and… | — | auto |
| [`typescript-toolchain`](skills/typescript-toolchain/SKILL.md) | TypeScript compiler workflow: tsconfig, module resolution, diagnostics, typecheck performance, JS-to-TS… | TypeScript compiler workflow: tsconfig, module resolution, diagnostics, typecheck performance, JS-to-TS migration, monorepo project… | — | auto |
| [`vitest`](skills/vitest/SKILL.md) | Vitest unit/integration testing: official API/config/coverage references plus practice patterns… | Use when writing or editing * | — | auto |
| [`workers-best-practices`](skills/workers-best-practices/SKILL.md) | Cloudflare Workers best practices for production applications | Use when writing, reviewing, or configuring Workers | — | auto |
| [`workers-profiling`](skills/workers-profiling/SKILL.md) | Profile or debug CPU usage and memory allocation in deployed Cloudflare Workers and Durable Objects | Profile or debug CPU usage and memory allocation in deployed Cloudflare Workers and Durable Objects. Then use this information to… | — | auto |

### Marketing strategy

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`co-marketing`](skills/co-marketing/SKILL.md) | Find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities | Use when the user says 'co-marketing,' 'partner marketing,' 'joint campaign,' 'who should we partner with,' 'integration marketing,'… | — | auto |
| [`competitor-profiling`](skills/competitor-profiling/SKILL.md) | Research, profile, or analyze competitors from their URLs | Use when the user mentions 'competitor profile,' 'competitor research,' 'competitor analysis,' 'profile this competitor,' 'analyze competitor,'… | — | auto |
| [`competitors`](skills/competitors/SKILL.md) | Competitor comparison or alternative pages for SEO and buyer-facing use, or structured competitive… | Use when the user mentions 'alternative page,' 'vs page,' 'competitor comparison,' 'comparison page,' '[Product] vs [Product],' '[Product]… | — | auto |
| [`content-strategy`](skills/content-strategy/SKILL.md) | Plan a content strategy, decide what content to create, or figure out what topics to cover | Use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," "content… | — | auto |
| [`copywriting`](skills/copywriting/SKILL.md) | Write, rewrite, or improve marketing copy for any page, including homepage, landing pages, pricing… | Use when the user says "write copy for," "improve this copy," "rewrite this page," "marketing copy," "headline help," "CTA copy," "value… | — | auto |
| [`customer-research`](skills/customer-research/SKILL.md) | Conduct, analyze, or synthesize customer research | Use when the user mentions "customer research," "ICP research," "talk to customers," "analyze transcripts," "customer interviews," "survey… | — | auto |
| [`launch`](skills/launch/SKILL.md) | Plan a product launch, feature announcement, or release strategy | Use when the user mentions 'launch,' 'Product Hunt,' 'feature release,' 'announcement,' 'go-to-market,' 'beta launch,' 'early access,'… | — | auto |
| [`marketing-council`](skills/marketing-council/SKILL.md) | Multiple expert perspectives on a marketing question — a simulated board of advisors staffed by… | Use when the user mentions 'marketing council,' 'board of advisors,' 'advisory board,' 'what would Seth Godin say,' 'what would Ogilvy think,'… | — | auto |
| [`marketing-ideas`](skills/marketing-ideas/SKILL.md) | Marketing ideas, inspiration, or strategies for their SaaS or software product | Use when the user asks for 'marketing ideas,' 'growth ideas,' 'how to market,' 'marketing strategies,' 'marketing tactics,' 'ways to promote,'… | — | auto |
| [`marketing-loops`](skills/marketing-loops/SKILL.md) | Set up a recurring, self-running marketing workflow — a repeatable loop an AI agent runs on a cadence… | Use when the user mentions 'marketing loop,' 'recurring marketing workflow,' 'automate my marketing,' 'marketing on autopilot,' 'weekly… | — | auto |
| [`marketing-plan`](skills/marketing-plan/SKILL.md) | Comprehensive marketing plan for a client, a company they advise, or their own product | Use when the user mentions "marketing plan," "growth plan," "GTM plan," "go-to-market plan," "AARRR plan," "90-day marketing plan," "12-month… | — | auto |
| [`marketing-psychology`](skills/marketing-psychology/SKILL.md) | Apply psychological principles, mental models, or behavioral science to marketing | Use when the user mentions 'psychology,' 'mental models,' 'cognitive bias,' 'persuasion,' 'behavioral science,' 'why people buy,'… | — | auto |
| [`offers`](skills/offers/SKILL.md) | Design, construct, or improve an offer — the thing they actually sell — including value framing, bonus… | Use when the user mentions 'offer,' 'offer design,' 'build an offer,' 'grand slam offer,' 'irresistible offer,' 'value stack,' 'bonus stack,'… | — | auto |
| [`pricing`](skills/pricing/SKILL.md) | Pricing decisions, packaging, or monetization strategy | Use when the user mentions 'pricing,' 'pricing tiers,' 'freemium,' 'free trial,' 'packaging,' 'price increase,' 'value metric,' 'Van… | — | auto |
| [`product-marketing`](skills/product-marketing/SKILL.md) | Create or update their product marketing context document | Use when the user mentions 'product context,' 'marketing context,' 'set up context,' 'positioning,' 'who is my target audience,' 'describe my… | — | auto |

### Ads & creative

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`ad-creative`](skills/ad-creative/SKILL.md) | Generate, iterate, or scale ad creative — headlines, descriptions, primary text, or full ad variations —… | Use when the user mentions 'ad copy variations,' 'ad creative,' 'generate headlines,' 'RSA headlines,' 'bulk ad copy,' 'creative testing,'… | — | auto |
| [`ads`](skills/ads/SKILL.md) | Paid advertising campaigns on Google Ads, Meta (Facebook/Instagram), LinkedIn, Twitter/X, or other ad… | Use when the user mentions 'PPC,' 'paid media,' 'ROAS,' 'CPA,' 'ad campaign,' 'retargeting,' 'audience targeting,' 'Google Ads,' 'Facebook ads,'… | — | auto |

### Growth surfaces

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`ab-testing`](skills/ab-testing/SKILL.md) | Plan, design, or implement an A/B test or experiment, or build a growth experimentation program | Use when the user mentions "A/B test," "split test," "experiment," "test this change," "variant copy," "multivariate test," "hypothesis,"… | — | auto |
| [`analytics`](skills/analytics/SKILL.md) | Set up, improve, or audit analytics tracking and measurement | Use when the user mentions "set up tracking," "GA4," "Google Analytics," "event tracking," "UTM parameters," "tag manager," "GTM," "analytics… | — | auto |
| [`churn-prevention`](skills/churn-prevention/SKILL.md) | Reduce churn, build cancellation flows, set up save offers, recover failed payments, or implement… | Use when the user mentions 'churn,' 'cancel flow,' 'offboarding,' 'save offer,' 'dunning,' 'failed payment recovery,' 'win-back,' 'retention,'… | — | auto |
| [`cold-email`](skills/cold-email/SKILL.md) | Write and run B2B cold outbound that gets replies, from cold emails and follow-ups to sending setup,… | Use when the user mentions "cold email," "cold outreach," "outbound," "prospecting email," "SDR emails," "follow-up sequence," "nobody's… | — | auto |
| [`cro`](skills/cro/SKILL.md) | Optimize, improve, or increase conversions on any marketing page or form — including homepage, landing… | Use when the user says 'CRO,' 'conversion rate optimization,' 'this page isn't converting,' 'improve conversions,' 'why isn't this page… | — | auto |
| [`emails`](skills/emails/SKILL.md) | Create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program | Use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement… | — | auto |
| [`onboarding`](skills/onboarding/SKILL.md) | Optimize post-signup onboarding, user activation, first-run experience, or time-to-value | Use when the user mentions "onboarding flow," "activation rate," "user activation," "first-run experience," "empty states," "onboarding… | — | auto |
| [`paywalls`](skills/paywalls/SKILL.md) | Create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates | Use when the user mentions "paywall," "upgrade screen," "upgrade modal," "upsell," "feature gate," "convert free to paid," "freemium… | — | auto |
| [`popups`](skills/popups/SKILL.md) | Create or optimize popups, modals, overlays, slide-ins, or banners for conversion purposes | Use when the user mentions "exit intent," "popup conversions," "modal optimization," "lead capture popup," "email popup," "announcement banner,"… | — | auto |
| [`referrals`](skills/referrals/SKILL.md) | Create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy | Use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' 'partner program,' 'referral… | — | auto |
| [`signup`](skills/signup/SKILL.md) | Optimize signup, registration, account creation, or trial activation flows | Use when the user mentions "signup conversions," "registration friction," "signup form optimization," "free trial signup," "reduce signup… | — | auto |
| [`sms`](skills/sms/SKILL.md) | Plan, build, or optimize SMS, MMS, or WhatsApp marketing — including welcome flows, abandoned cart… | Use when the user mentions "SMS marketing," "text message campaigns," "SMS sequence," "SMS automation," "abandoned cart text," "post-purchase… | — | auto |

### SEO & discovery

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`ai-seo`](skills/ai-seo/SKILL.md) | Optimize content for AI search engines, get cited by LLMs, or appear in AI-generated answers | Use when the user mentions 'AI SEO,' 'AEO,' 'GEO,' 'LLMO,' 'answer engine optimization,' 'generative engine optimization,' 'LLM optimization,'… | — | auto |
| [`programmatic-seo`](skills/programmatic-seo/SKILL.md) | Create SEO-driven pages at scale using templates and data | Use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city]… | — | auto |
| [`schema`](skills/schema/SKILL.md) | Add, fix, or optimize schema markup and structured data on their site | Use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema | — | auto |
| [`seo-audit`](skills/seo-audit/SKILL.md) | Audit, review, or diagnose SEO issues on their site | When the user asks to improve SEO, fix meta tags, add structured data, or optimize a sitemap | — | auto |
| [`site-architecture`](skills/site-architecture/SKILL.md) | Plan, map, or restructure their website's page hierarchy, navigation, URL structure, or internal linking | Use when the user mentions "sitemap," "site map," "visual sitemap," "site structure," "page hierarchy," "information architecture," "IA,"… | — | auto |

### Sales & RevOps

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`prospecting`](skills/prospecting/SKILL.md) | Find, qualify, and build a list of prospects to reach out to, across B2B SaaS, general B2B, or local… | Use when the user mentions "prospecting," "build a prospect list," "find leads," "lead list," "outbound list," "target account list," "ICP-fit… | — | auto |
| [`revops`](skills/revops/SKILL.md) | Revenue operations, lead lifecycle management, or marketing-to-sales handoff processes | Use when the user mentions 'RevOps,' 'revenue operations,' 'lead scoring,' 'outbound pipeline stages,' 'lead routing,' 'MQL,' 'SQL,' 'pipeline… | — | auto |
| [`sales-enablement`](skills/sales-enablement/SKILL.md) | Create sales collateral, pitch decks, one-pagers, objection handling docs, or demo scripts | Use when the user mentions 'sales deck,' 'pitch deck,' 'one-pager,' 'leave-behind,' 'objection handling,' 'deal-specific ROI analysis,' 'demo… | — | auto |

### Creative media

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`image`](skills/image/SKILL.md) | Create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product… | Use when the user mentions 'AI image generation,' 'generate an image,' 'create a graphic,' 'product mockup,' 'hero image,' 'social media… | — | auto |

### Symlink stubs (content not in this checkout)

These directories are symlinks to `../../.agents/skills/...`, which is not present here. They do not currently load.

| Skill | Intended area | Symlink target |
|-------|---------------|----------------|
| `higgsfield-brandkit` | Creative media | `../../.agents/skills/higgsfield-brandkit` |
| `higgsfield-faceless-video` | Creative media | `../../.agents/skills/higgsfield-faceless-video` |
| `higgsfield-generate` | Creative media | `../../.agents/skills/higgsfield-generate` |
| `higgsfield-marketplace-cards` | Creative media | `../../.agents/skills/higgsfield-marketplace-cards` |
| `higgsfield-product-photoshoot` | Creative media | `../../.agents/skills/higgsfield-product-photoshoot` |
| `higgsfield-soul-id` | Creative media | `../../.agents/skills/higgsfield-soul-id` |
| `higgsfield-video-explainer` | Creative media | `../../.agents/skills/higgsfield-video-explainer` |
| `higgsfield-websites` | Creative media | `../../.agents/skills/higgsfield-websites` |
| `higgsfield-youtube-thumbnail` | Creative media | `../../.agents/skills/higgsfield-youtube-thumbnail` |
| `connect-recommend` | Vendor APIs | `../../.agents/skills/connect-recommend` |
| `connect-required-verification-information` | Vendor APIs | `../../.agents/skills/connect-required-verification-information` |
| `metronome` | Vendor APIs | `../../.agents/skills/metronome` |
| `stripe-apps` | Vendor APIs | `../../.agents/skills/stripe-apps` |
| `stripe-best-practices` | Vendor APIs | `../../.agents/skills/stripe-best-practices` |
| `stripe-directory` | Vendor APIs | `../../.agents/skills/stripe-directory` |
| `stripe-docs` | Vendor APIs | `../../.agents/skills/stripe-docs` |
| `stripe-pay` | Vendor APIs | `../../.agents/skills/stripe-pay` |
| `stripe-projects` | Vendor APIs | `../../.agents/skills/stripe-projects` |
| `upgrade-stripe` | Vendor APIs | `../../.agents/skills/upgrade-stripe` |

