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
| `~/.agents/skills` | `skills/` (the shared folder `npx skills add -g` installs into; opencode reads it) |
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

117 skills with local `SKILL.md` content under `skills/`.

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
| [`brainstorming`](skills/brainstorming/SKILL.md) | Explore unclear product or design intent before building | When the user asks to brainstorm, shape a design, or clarify what to build | — | auto |
| [`codebase-design`](skills/codebase-design/SKILL.md) | Shared vocabulary for designing deep modules | Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more… | — | auto |
| [`constraint-driven-development`](skills/constraint-driven-development/SKILL.md) | Establishes a project's quality bar as a written contract and stops agents quietly lowering it.… | Use when no quality bar is written down, when the user says "set up constraints" or "define our standards", when the user wants dimensions they… | — | auto |
| [`design-doc-mermaid`](skills/design-doc-mermaid/SKILL.md) | Create Mermaid diagrams (flowchart, sequence, class, ER, state, C4, architecture) from text or source… | Mermaid fences for docs/README/GitHub; prefer over Excalidraw for documentation | — | auto |
| [`domain-modeling`](skills/domain-modeling/SKILL.md) | Build and sharpen a project's domain model | Use when discussing codebase terminology or writing or editing a GLOSSARY.md; ADRs go to architecture-decision-records | — | auto |
| [`doubt-driven-development`](skills/doubt-driven-development/SKILL.md) | Subjects non-trivial decisions to a fresh-context adversarial review before they stand | Use when stress-testing a plan, working in unfamiliar code, stakes are high (auth, security, migration, irreversible ops), or a confident output… | — | auto |
| [`excalidraw-diagram-generator`](skills/excalidraw-diagram-generator/SKILL.md) | Generate Excalidraw whiteboard diagrams as `.excalidraw` JSON | Excalidraw file / editable whiteboard / mind map; not Mermaid docs (use design-doc-mermaid) | — | auto |
| [`grill-with-docs`](skills/grill-with-docs/SKILL.md) | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go | Manual only (`/grill-with-docs`). Not auto-matched from conversation. | `/grill-with-docs` | slash-only |
| [`grilling`](skills/grilling/SKILL.md) | Grill the user relentlessly about a plan, decision, or idea until shared understanding | Use when the ask is underspecified, when the user wants to stress-test thinking, or uses grill/interview triggers ("grill me", "interview me",… | — | auto |
| [`how`](skills/how/SKILL.md) | "how does X work", code walkthroughs before changing something, and placement / ownership / layering… | Manual only (`/how`). Not auto-matched from conversation. | `/how` | slash-only |
| [`i-have-adhd`](skills/i-have-adhd/SKILL.md) | Shape output for a reader with ADHD: lead with the next action, number multi-step work, restate state… | Invoke with /i-have-adhd; stays on until "stop adhd mode" | `/i-have-adhd` | slash-only |
| [`improve-codebase-architecture`](skills/improve-codebase-architecture/SKILL.md) | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through… | Manual only (`/improve-codebase-architecture`). Not auto-matched from conversation. | `/improve-codebase-architecture` | slash-only |
| [`incremental-implementation`](skills/incremental-implementation/SKILL.md) | Delivers changes in thin, verifiable slices, and breaks oversized work into ordered tasks with… | Use when implementing multi-file changes, picking up the next task from a plan, writing a plan from a spec, rolling out behind a feature flag,… | — | auto |
| [`local-worker`](skills/local-worker/SKILL.md) | Delegate a checkable task to a local opencode agent on Ollama, then review and correct its work | When the user asks to use a local model, local agent, local subagent, opencode, or an Ollama worker, or to save frontier tokens on mechanical work | `/local-worker` | auto |
| [`prd`](skills/prd/SKILL.md) | Generate PRDs and AI-ready `/spec/` specification files for software and AI-powered features | Write a PRD, document requirements, plan a feature, or create a Generative-AI consumption file under `/spec/` | — | auto |
| [`source-driven-development`](skills/source-driven-development/SKILL.md) | Ground framework-specific decisions in official documentation for the installed versions | Use when correctness depends on a framework/library API or recommended pattern, when building boilerplate that will be copied, or when the user… | — | auto |
| [`test-driven-development`](skills/test-driven-development/SKILL.md) | Drives development with the red-green-refactor loop | Use when implementing new logic or behavior, fixing bugs (prove-it with a failing test first), or changing existing behavior in a maintained… | — | auto |
| [`why`](skills/why/SKILL.md) | 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or… | Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds | `/why` | slash-only |

### Code quality & review

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`blast-radius`](skills/blast-radius/SKILL.md) | Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact… | Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust | `/blast-radius` | slash-only |
| [`ci-cd-and-automation`](skills/ci-cd-and-automation/SKILL.md) | Automates CI/CD pipeline setup | Use when setting up or modifying build and deployment pipelines | — | auto |
| [`code-review`](skills/code-review/SKILL.md) | Review changes since a fixed point (commit, branch, tag, or merge-base) on two axes: Standards (repo… | Use when reviewing a branch, a PR, WIP changes, or "review since X" | — | auto |
| [`code-simplification`](skills/code-simplification/SKILL.md) | Simplify working code for clarity without changing behavior | Simplify / reduce nesting / readability refactor; not AI-slop PR cleanup (deslop) or prose (unslop) | — | auto |
| [`deprecation-and-migration`](skills/deprecation-and-migration/SKILL.md) | Manages deprecation and migration | Use when removing old systems, APIs, or features | — | auto |
| [`deslop`](skills/deslop/SKILL.md) | Remove AI-generated code slop on a branch or diff without changing behavior | Deslop / AI code noise on a PR; not general simplify (code-simplification) or prose (unslop) | — | auto |
| [`git-commit`](skills/git-commit/SKILL.md) | Making a Git commit or splitting changes into more than one commit | When the user asks to commit or types /commit, or when standing global/project Git instructions approve committing after validation | `/commit` | auto |
| [`make-pr-easy-to-review`](skills/make-pr-easy-to-review/SKILL.md) | Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer… | Prepare PRs for review by cleaning noisy history, improving PR descriptions, and adding reviewer guidance without changing code… | — | auto |
| [`observability-and-instrumentation`](skills/observability-and-instrumentation/SKILL.md) | Instruments code so production behavior is visible and diagnosable | Use when adding logging, metrics, tracing, or alerting | — | auto |
| [`security-and-hardening`](skills/security-and-hardening/SKILL.md) | Hardens code against vulnerabilities; includes TypeScript/Node review references | Auditing input/auth/storage/integrations, OWASP checks, dependency risk, privacy; TS/Node XSS/JWT/injection reviews | — | auto |
| [`shipping-and-launch`](skills/shipping-and-launch/SKILL.md) | Prepares engineering production deploys | Eng deploy / staged rollout / monitoring / rollback; not marketing GTM (launch) | — | auto |
| [`technical-writing`](skills/technical-writing/SKILL.md) | Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE… | Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages | `/technical-writing` | slash-only |
| [`thermo-nuclear-code-quality-review`](skills/thermo-nuclear-code-quality-review/SKILL.md) | Run an extremely strict maintainability review for abstraction quality, giant files, and… | Manual only (`/thermo-nuclear-code-quality-review`). Not auto-matched from conversation. | `/thermo-nuclear-code-quality-review` | slash-only |
| [`unslop`](skills/unslop/SKILL.md) | Cut AI tells from any writing | Manual only (`/unslop`). Not auto-matched from conversation. | `/unslop` | slash-only |

### Frontend & design

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`accessibility`](skills/accessibility/SKILL.md) | Deep WCAG 2.2 accessibility audit and remediation | a11y audit / WCAG / screen reader / keyboard remediation as the primary ask | — | auto |
| [`browser-testing-with-devtools`](skills/browser-testing-with-devtools/SKILL.md) | Verifies UI in a real browser with Cursor browser / CDP tools | Use when building or debugging anything that renders in a browser, inspecting the DOM, capturing console errors, analyzing network requests,… | — | auto |
| [`frontend-design`](skills/frontend-design/SKILL.md) | Distinctive intentional visual design / anti-slop art direction | Landing/marketing/product UI redesign; defers eng states, WCAG audits, and polish | — | auto |
| [`frontend-ui-engineering`](skills/frontend-ui-engineering/SKILL.md) | Production-quality responsive UI engineering (states, loading, baseline a11y) | Building/modifying interfaces with eng depth; deep WCAG audits go to accessibility | — | auto |
| [`image-to-code`](skills/image-to-code/SKILL.md) | Opt-in image-first website design: generate design image(s), analyze them, then implement | Manual only (`/image-to-code`). Not auto-matched from conversation. | `/image-to-code` | slash-only |
| [`modern-web-guidance`](skills/modern-web-guidance/SKILL.md) | Look up current vanilla web-platform / HTML / CSS / DOM capability guides | Platform-capability lookup via npx tool; not mandatory for every React UI task | — | auto |
| [`polish`](skills/polish/SKILL.md) | Final quality pass for alignment, spacing, consistency, states, and micro-detail | Polish / finishing touches / UI micro-detail; not redesign or WCAG audits | — | auto |
| [`prototype`](skills/prototype/SKILL.md) | Build a throwaway prototype to answer a design question | Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like | — | auto |
| [`tailwind-design-system`](skills/tailwind-design-system/SKILL.md) | Build scalable design systems with Tailwind CSS v4, design tokens, component libraries, and responsive… | Use when creating component libraries, implementing design systems, or standardizing UI patterns | — | auto |
| [`web-perf`](skills/web-perf/SKILL.md) | Audit, diagnose, or optimize loading and interaction performance | Use when measure-first profiling points at frontend, backend, or query bottlenecks | — | auto |

### Platform & backend

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`cf-cli`](skills/cf-cli/SKILL.md) | Cloudflare's official cf CLI (beta) for the public Cloudflare API and Workers projects | Cloudflare's official cf CLI (beta) for the public Cloudflare API and Workers projects. Use for finding and running Cloudflare commands… | — | auto |
| [`chrome-extensions`](skills/chrome-extensions/SKILL.md) | Build and publish Chrome Extensions using Manifest V3 best practices | Phrases like: 'Chrome extension'; 'browser extension'; 'manifest.json' | — | auto |
| [`cloudflare`](skills/cloudflare/SKILL.md) | Discover and choose Cloudflare products for apps, APIs, AI agents, storage, networking, and security | Discover and choose Cloudflare products for apps, APIs, AI agents, storage, networking, and security. Use for architecture and product… | — | auto |
| [`cloudflare-email-service`](skills/cloudflare-email-service/SKILL.md) | Implement or troubleshoot Cloudflare Email Sending and Email Routing integrations and their delivery… | Implement or troubleshoot Cloudflare Email Sending and Email Routing integrations and their delivery configuration. | — | auto |
| [`connect-recommend`](skills/connect-recommend/SKILL.md) | Stripe Connect setup guidance: configuration, charge patterns, Dashboard access, getting started | Use this skill when the user asks about Stripe Connect configuration, charge patterns, Dashboard access, or how to get started with… | none | auto |
| [`connect-required-verification-information`](skills/connect-required-verification-information/SKILL.md) | What a Stripe Connect connected account must provide for verification and onboarding | Use this skill when the user asks what information a Stripe Connect connected account must provide for verification, onboarding, KYC, or… | none | auto |
| [`durable-objects`](skills/durable-objects/SKILL.md) | Build, debug, or review Cloudflare Durable Objects code for persistent state and coordination | Build, debug, or review Cloudflare Durable Objects code for persistent state and coordination. | — | auto |
| [`metronome`](skills/metronome/SKILL.md) | Guides Metronome usage-based billing integration decisions: event ingestion (single and batch,… | Use when building, modifying, or reviewing any Metronome integration, including ingesting usage events, creating customers, contracts, or… | none | auto |
| [`nestjs-best-practices`](skills/nestjs-best-practices/SKILL.md) | NestJS best practices and architecture patterns for building production-ready applications | NestJS best practices and architecture patterns for building production-ready applications. This skill should be used when writing,… | — | auto |
| [`nextjs-on-cloudflare`](skills/nextjs-on-cloudflare/SKILL.md) | Build, migrate, and deploy Next.js apps on Cloudflare Workers with vinext | Use when starting a Next | — | auto |
| [`nextjs-react`](skills/nextjs-react/SKILL.md) | Next.js App Router and React TypeScript patterns: Server Components, client boundaries, data fetching,… | Use when editing Next | — | auto |
| [`postgres`](skills/postgres/SKILL.md) | PostgreSQL schema design, indexing, query patterns, operations (pooling, replication, upgrades), table… | Use when writing SQL, designing schemas, optimizing queries, reviewing migrations, or debugging Postgres performance | — | auto |
| [`postgres-drizzle`](skills/postgres-drizzle/SKILL.md) | Write or review Drizzle ORM schemas, relations, queries, and drizzle-kit migrations | Drizzle/drizzle-kit code; vendor-neutral SQL/ops go to postgres | — | auto |
| [`stripe-apps`](skills/stripe-apps/SKILL.md) | Build, modify, or review Stripe Apps and extensions using the relevant documentation and reference… | Build, modify, or review Stripe Apps and extensions using the relevant documentation and reference guides. | none | auto |
| [`stripe-best-practices`](skills/stripe-best-practices/SKILL.md) | Guides Stripe integration decisions across development and test environment planning (separate… | Use when planning, building, modifying, testing, or reviewing any Stripe integration, including choosing a development environment,… | none | auto |
| [`stripe-directory`](skills/stripe-directory/SKILL.md) | Identifies external providers, merchants, nonprofits, platforms, APIs, and software services, and… | Identifies external providers, merchants, nonprofits, platforms, APIs, and software services, and resolves the documented way to engage… | none | auto |
| [`stripe-docs`](skills/stripe-docs/SKILL.md) | Read and search Stripe documentation and API reference | Use when the user or agent needs to read, search, or look up Stripe documentation or API reference | none | auto |
| [`stripe-pay`](skills/stripe-pay/SKILL.md) | Helps users send funds to another Stripe business, transfer money to a Stripe Profile handle or… | Helps users send funds to another Stripe business, transfer money to a Stripe Profile handle or network ID, or ask whether an agent can pay… | none | auto |
| [`stripe-projects`](skills/stripe-projects/SKILL.md) | Provision infrastructure and third-party services with Stripe Projects | Use when the user wants to provision infrastructure or third-party services using Stripe Projects | none | auto |
| [`typescript-best-practices`](skills/typescript-best-practices/SKILL.md) | Daily TypeScript coding rules plus advanced type-level design (generics, conditional, mapped, template literal types) | Use when reading or editing TypeScript | — | auto |
| [`typescript-docs`](skills/typescript-docs/SKILL.md) | TypeScript API documentation with JSDoc, TypeDoc, and framework examples | Public TS API docs; ADRs go to architecture-decision-records | — | auto |
| [`typescript-toolchain`](skills/typescript-toolchain/SKILL.md) | TypeScript compiler workflow: tsconfig, module resolution, diagnostics, typecheck performance, JS-to-TS… | TypeScript compiler workflow: tsconfig, module resolution, diagnostics, typecheck performance, JS-to-TS migration, monorepo project… | — | auto |
| [`upgrade-stripe`](skills/upgrade-stripe/SKILL.md) | Guide for upgrading Stripe API versions, webhook endpoints, server-side SDKs, Stripe.js, and mobile… | Guide for upgrading Stripe API versions, webhook endpoints, server-side SDKs, Stripe.js, and mobile SDKs | none | auto |
| [`vitest`](skills/vitest/SKILL.md) | Vitest unit/integration testing: official API/config/coverage references plus practice patterns… | Use when writing or editing * | — | auto |
| [`workers-best-practices`](skills/workers-best-practices/SKILL.md) | Cloudflare Workers best practices for production applications | Use when writing, reviewing, or configuring Workers | — | auto |
| [`workers-profiling`](skills/workers-profiling/SKILL.md) | Profile or debug CPU usage and memory allocation in deployed Cloudflare Workers and Durable Objects | Profile or debug CPU usage and memory allocation in deployed Cloudflare Workers and Durable Objects. Then use this information to… | — | auto |

### Marketing strategy

| Skill | Purpose | Activates when | Command | Mode |
|-------|---------|----------------|---------|------|
| [`co-marketing`](skills/co-marketing/SKILL.md) | Find co-marketing partners, plan joint campaigns, or brainstorm partnership opportunities | Use when the user says 'co-marketing,' 'partner marketing,' 'joint campaign,' 'who should we partner with,' 'integration marketing,'… | — | auto |
| [`competitor-profiling`](skills/competitor-profiling/SKILL.md) | Research, profile, or analyze competitors from their URLs; teardowns, SWOT, feature matrices | Use when the user mentions 'competitor profile,' 'competitor research,' 'competitor analysis,' 'competitor teardown,' 'SWOT,' 'feature matrix'… | — | auto |
| [`competitors`](skills/competitors/SKILL.md) | Competitor comparison or alternative pages for SEO and buyer-facing use | Use when the user mentions 'alternative page,' 'vs page,' 'competitor comparison,' 'comparison page,' '[Product] vs [Product],' '[Product]… | — | auto |
| [`content-strategy`](skills/content-strategy/SKILL.md) | Plan a content strategy, decide what content to create, or figure out what topics to cover | Use when the user mentions "content strategy," "what should I write about," "content ideas," "blog strategy," "topic clusters," "content… | — | auto |
| [`copywriting`](skills/copywriting/SKILL.md) | Write, rewrite, or improve marketing copy for any page, including homepage, landing pages, pricing… | Use when the user says "write copy for," "improve this copy," "rewrite this page," "marketing copy," "headline help," "CTA copy," "value… | — | auto |
| [`customer-research`](skills/customer-research/SKILL.md) | Conduct, analyze, or synthesize customer research | Use when the user mentions "customer research," "ICP research," "talk to customers," "analyze transcripts," "customer interviews," "survey… | — | auto |
| [`launch`](skills/launch/SKILL.md) | Plan a product launch, feature announcement, or marketing GTM release | Product Hunt / GTM / announcement / marketing launch checklist; not eng deploy (shipping-and-launch) | — | auto |
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
| [`higgsfield-brandkit`](skills/higgsfield-brandkit/SKILL.md) | Create and extend complete visual brand systems through the Higgsfield CLI and bundled… | Use when: "create a brand kit", "make a visual identity", "design a logo and brandbook", "apply this logo to branded assets", "make… | none | auto |
| [`higgsfield-faceless-video`](skills/higgsfield-faceless-video/SKILL.md) | Create a finished faceless explainer, documentary, illustrated story or children's music video, or… | Use when: "make a faceless video", "create a narrated explainer", "make a children's song video", "edit this faceless video" | none | auto |
| [`higgsfield-generate`](skills/higgsfield-generate/SKILL.md) | Generate images/videos/3D assets/audio via Higgsfield AI | Use when: "generate an image", "make a video", "animate this photo", "image-to-video", "edit/stylize/remix this image", "reframe this… | none | auto |
| [`higgsfield-marketplace-cards`](skills/higgsfield-marketplace-cards/SKILL.md) | Generate marketplace product image cards through Higgsfield: compliant main image, secondary… | Use when the user asks for marketplace listing images, product detail cards, secondary product images, product infographics, lifestyle… | none | auto |
| [`higgsfield-product-photoshoot`](skills/higgsfield-product-photoshoot/SKILL.md) | Generate brand-quality product images through Higgsfield product-photoshoot prompt enhancement on… | Use when: "product photo", "studio shot", "lifestyle image", "Pinterest pin", "hero/banner", "carousel", "ad creative", "Meta ads",… | none | auto |
| [`higgsfield-soul-id`](skills/higgsfield-soul-id/SKILL.md) | Train a Soul Character, a personalized model on a person's face that Higgsfield uses for… | Use when: "create my Soul", "train my face", "make my digital twin", "build me an avatar", "learn my appearance", "create a character of… | none | auto |
| [`higgsfield-video-explainer`](skills/higgsfield-video-explainer/SKILL.md) | Compatibility entry for the former video explainer skill | Use when: the user explicitly invokes higgsfield-video-explainer or continues its existing workflow | none | auto |
| [`higgsfield-websites`](skills/higgsfield-websites/SKILL.md) | Build, edit, and deploy full-stack websites, apps and games via the Higgsfield CLI (`higgsfield… | Use when: "build me a website", "make a landing page", "create a web app", "build a SaaS dashboard / portfolio", "make me a game", "deploy… | none | auto |
| [`higgsfield-youtube-thumbnail`](skills/higgsfield-youtube-thumbnail/SKILL.md) | Create high-click-through YouTube thumbnails and vertical video covers through the Higgsfield CLI | Use when: "make a YouTube thumbnail", "thumbnail for this video", "MrBeast-style cover", "Shorts cover", or "Instagram video cover" | none | auto |
| [`image`](skills/image/SKILL.md) | Create, generate, edit, or optimize images for marketing — blog heroes, social graphics, product… | Use when the user mentions 'AI image generation,' 'generate an image,' 'create a graphic,' 'product mockup,' 'hero image,' 'social media… | — | auto |

