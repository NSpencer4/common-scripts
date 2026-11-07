# Handoff - global AI skills and marketing-plan stack

Use this when starting a new agent chat. Repo: `~/WebstormProjects/common-scripts`, branch `chore/centralize-ai-globals`, draft PR https://github.com/NSpencer4/common-scripts/pull/1

## What we built

### Shared globals (revision-controlled)

Canonical copies live in this repo. Local AI tools symlink here (do not re-copy into `~/.cursor/skills` etc.):

| Path | Target |
|------|--------|
| `~/.cursor/skills` | `common-scripts/skills/` |
| `~/.claude/skills` | same |
| `~/.codex/skills` | same |
| `~/.config/opencode/skills` | same |
| `~/.junie/skills` | same |
| `~/.agents/skills` | same |
| `~/.claude/AGENTS.md` (+ `CLAUDE.md` → it) | `common-scripts/AGENTS.md` |
| `~/.codex|opencode|junie/AGENTS.md` | same |
| `~/.cursor/rules/global.mdc` | `common-scripts/cursor/rules/global.mdc` |

Linker for other machines: `scripts/link-ai-globals.sh`. Prior copies backed up under `~/.ai-globals-backup-*`.

`npx skills add -g` into those agents writes into this repo via the symlinks. There is no skills.sh setting for a custom install root.

### Skills install policy (from long skills.sh session)

- Install **statically** (copy `SKILL.md` + refs + `SOURCE.md`). Do **not** use `npx skills` as the install method when adapting.
- Merge overlaps when Chase picks options; ask before installing on conflicts.
- Strip install scripts / pipe-to-shell / phone-home; omit risky helpers (e.g. Excalidraw `.py`).
- Soften third-party CLI coupling (inference.sh, pstack `arena`/`poteto-mode`, etc.) when installing.

Earlier skill batches also live under personal skill roots historically; **this repo is now the source of truth.**

### Marketing-plan composition (just installed)

For marketing strategy / plan talk, intended stack:

1. **`product-marketing`** - foundation; creates/updates `.agents/product-marketing.md`
2. **`marketing-plan`** - AARRR / 12-month / fCMO plan hub (auto-trigger via description; slash `/marketing-plan` optional)
3. Inputs: **`marketing-ideas`**, **`customer-research`**, **`competitor-profiling`**, **`marketing-psychology`**, **`offers`**, **`marketing-council`**
4. Channel depth (also installed where missing): `ads`, `ad-creative`, `content-strategy`, `cro`, `churn-prevention`, `programmatic-seo`, `schema`, `revops`, `prospecting`, `paywalls`
5. Already had many channels: `seo-audit`, `ai-seo`, `signup`, `onboarding`, `emails`, `referrals`, `pricing`, `launch`, `copywriting`, `cold-email`, etc.

Chase prefers **auto skill use** from conversation match, not required slash commands. Open tweak: soften `marketing-plan` "invoke with `/marketing-plan`" docs and ensure it runs `product-marketing` when `.agents/product-marketing.md` is missing.

### cursor/plugins (reviewed)

Marketplace of many plugins; do **not** `npx skills add cursor/plugins` wholesale.

**Already had:** `unslop`, `how`, `why`, `technical-writing`, `architect`, `typescript-best-practices`

**Taken:**
- `deslop` (code slop; complements `unslop`)
- `blast-radius` (opt-in; prove breakage beyond callers; no pstack arena requirement)
- `make-pr-easy-to-review` (no force-push to protected branches)
- `thermo-nuclear-code-quality-review` (opt-in harsh maintainability; complements `code-review`)

**Merged into AGENTS / global.mdc:** prove-it-works, subtract-before-add, test-behavior, fix-root-causes, type/boundary discipline (as Engineering principles bullets)

**Skip:** full pack; pstack stack (`arena`, `poteto-mode`, `setup-pstack`, `bro`, `swarm`); ralph/ketchup/orchestrate; dyl-stack; teaching/continual-learning; SaaS MCP skills until needed; duplicate `tdd` / `interrogate`

### leonxlnx/taste-skill (reviewed)

Live upstream skill is `design-taste-frontend` (repo folder `skills/taste-skill`). Classics, imagegen, and `full-output-enforcement` moved or were removed.

**Direction taken:**
- Keep art direction in **`frontend-design`** (Anthropic + taste refs + product hard rules; no `draw.mjs` / `inspect.mjs`)
- Keep **`image-to-code`** opt-in only
- Fold redesign route into `frontend-design` (retired `redesign-existing-projects`)
- Short **Completeness** bullets in `AGENTS.md` / `cursor/rules/global.mdc` (from full-output idea; no separate skill)
- Skip: parallel `design-taste-frontend`, aesthetic presets (minimalist/brutalist/gpt-taste), imagegen reinstalls, global `stitch-design-taste`, full pack / scripts

### addyosmani/agent-skills (reviewed)

Already had (adapted earlier): `security-and-hardening`, `frontend-ui-engineering`, `code-simplification`, `incremental-implementation`, `deprecation-and-migration`, `source-driven-development`.

**Taken (static install, adapted):**
- `test-driven-development` (+ bundled `references/testing-patterns.md`)
- `doubt-driven-development`
- `observability-and-instrumentation` (+ bundled `references/observability-checklist.md`)
- `ci-cd-and-automation`
- `constraint-driven-development` (+ `scripts/quality-gate.mjs`, `references/floor-guard.md`)
- `browser-testing-with-devtools` (Cursor browser/CDP first)
- `shipping-and-launch` (eng deploy readiness; distinct from marketing `launch`)

**Skip:** `using-agent-skills`, `context-engineering`, full pack / `npx` install.

**Merged into existing skills:**
- `code-review-and-quality` → `code-review` (`references/five-axis-and-sizing.md`)
- `performance-optimization` → `web-perf` (measure-first + optimization-patterns)
- `debugging-and-error-recovery` → `debugging-strategies` (stop-the-line triage; skill later removed, AGENTS.md Debugging section covers it)
- `api-and-interface-design` → `api-design-principles` (Hyrum/contracts/boundaries; skill later removed)
- `documentation-and-adrs` → `architecture-decision-records` + `technical-writing`
- `spec-driven-development` → `prd` gated workflow (+ `/spec/` template under `prd/references/ai-ready-spec-template.md`)
- `planning-and-task-breakdown` → `incremental-implementation`
- `git-workflow-and-versioning` → selective `git-commit` change-sizing (no always-commit)
- `interview-me` → `grilling` (frontier UX kept; hypothesis/intent added)
- `idea-refine` → `brainstorming` (no shell helper)

## Related context (other repos)

- `atomic-presentational-ui` was removed from this repo; launch-sequence keeps its own copies under `.agents/skills`, `.cursor/skills`, and local `.claude/skills`.

- **launch-sequence** still on `docs/atomic-presentational-ui-skill` (PR #38) for atomic UI skill / AGENTS slim-down. That branch is **not** on common-scripts; migration mistakenly tried to check it out here once (checkpoint kept as `backup/checkpoint-before-atomic-checkout`).
- Bakery WIP was stashed earlier on launch-sequence as `wip bakery/tweaks before atomic-ui skill` (verify with `git stash list` there if needed).

## Sensible next changes

- Widen/soften marketing skill descriptions for auto-routing; wire `marketing-plan` → require/create product-marketing context first.
- Continue installing remaining marketingskills (social, video, events, ...) only as plans need them.
- Keep iterating skills **in this repo**, then commit/push on `chore/centralize-ai-globals`.
- Merge PR #1 when ready; avoid editing skills only under `~/.cursor/skills` (it is a symlink).

## Git status snapshot (at handoff)

- Branch: `chore/centralize-ai-globals` tracking `origin/chore/centralize-ai-globals`
- Recent commits: centralize globals; marketing-plan composition; addyosmani take-set; merge queue
- Local `main` may still be ahead of `origin/main` by the checkpoint commit; feature branch is the working line
