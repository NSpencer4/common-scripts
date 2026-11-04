# Handoff — global AI skills & marketing-plan stack

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

1. **`product-marketing`** — foundation; creates/updates `.agents/product-marketing.md`
2. **`marketing-plan`** — AARRR / 12-month / fCMO plan hub (auto-trigger via description; slash `/marketing-plan` optional)
3. Inputs: **`marketing-ideas`**, **`customer-research`**, **`competitor-profiling`**, **`marketing-psychology`**, **`offers`**, **`marketing-council`**
4. Channel depth (also installed where missing): `ads`, `ad-creative`, `content-strategy`, `cro`, `churn-prevention`, `programmatic-seo`, `schema`, `revops`, `prospecting`, `paywalls`
5. Already had many channels: `seo-audit`, `ai-seo`, `signup`, `onboarding`, `emails`, `referrals`, `pricing`, `launch`, `copywriting`, `cold-email`, etc.

Chase prefers **auto skill use** from conversation match, not required slash commands. Open tweak: soften `marketing-plan` “invoke with `/marketing-plan`” docs and ensure it runs `product-marketing` when `.agents/product-marketing.md` is missing.

## Related context (other repos)

- **launch-sequence** still on `docs/atomic-presentational-ui-skill` (PR #38) for atomic UI skill / AGENTS slim-down. That branch is **not** on common-scripts; migration mistakenly tried to check it out here once (checkpoint kept as `backup/checkpoint-before-atomic-checkout`).
- Bakery WIP was stashed earlier on launch-sequence as `wip bakery/tweaks before atomic-ui skill` (verify with `git stash list` there if needed).

## Sensible next changes

- Widen/soften marketing skill descriptions for auto-routing; wire `marketing-plan` → require/create product-marketing context first.
- Continue installing remaining marketingskills (social, video, events, …) only as plans need them.
- Keep iterating skills **in this repo**, then commit/push on `chore/centralize-ai-globals`.
- Merge PR #1 when ready; avoid editing skills only under `~/.cursor/skills` (it is a symlink).

## Git status snapshot (at handoff)

- Branch: `chore/centralize-ai-globals` tracking `origin/chore/centralize-ai-globals`
- Recent commits: centralize globals; add marketing-plan composition
- Local `main` may still be ahead of `origin/main` by the checkpoint commit; feature branch is the working line
