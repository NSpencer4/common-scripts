---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Produce architectural explanations at the level of a senior engineer onboarding onto a subsystem, enough to build a working mental model, not so much that it reads like annotated source code.

Every spawn is a Task subagent with `subagent_type: generalPurpose` and `readonly: true`. Explorers use the `how explorer` line in the `pstack-models.mdc` rule (default `grok-4.7-xhigh-fast`), and every explainer uses the `how explainer` line (default `claude-opus-5-5-xhigh`). Prefer the host default or an explicitly available model slug. If a suggested slug is rejected, use the closest valid model and say so. Pick each subagent's reasoning effort for the job. If **poteto-mode** is not installed, use sensible defaults (higher effort for synthesis, lower for parallel explore).



## Runtime adaptations (this install)

This snapshot is decoupled from the full Cursor pstack plugin pack.

- **Models:** Ignore `pstack-models.mdc` and **poteto-mode** if absent. When spawning subagents, use the host's Task/subagent tool with an available model (prefer a strong model for synthesis/explain; a cheaper/faster model for parallel explore/investigate). If a named slug is rejected, pick the closest available model and say so.
- **Missing sibling skills:** `arena`, `interrogate`, and `principle-*` skills are optional. If missing: for "design it twice," spawn two parallel sketch subagents yourself and synthesize; for adversarial pressure, use `grilling` or a critical review pass; treat named principles as plain guidance, not required skill loads.
- **MCP investigators (`why`):** Discover whatever MCPs exist. Skip categories with no MCP and record the gap. Always run source-control investigation via git/`gh`.
- **Cross-links:** Pair with `codebase-design` (module depth vocabulary), `architecture-patterns` (Clean/Hexagonal/DDD patterns), and `architecture-decision-records` (durable decision write-ups). `architect` grounds with `how`/`why`; ADRs capture the agreed decision afterward when the change is significant.

## 1. Assess complexity

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

- **Simple** (a single module, a small utility, a narrow question such as "how does function X work"): no explorers. Spawn one explainer that explores and explains in one pass, built from `references/explainer-prompt.md` without the explorer-findings section. Go to step 4.
- **Complex** (a subsystem spanning multiple files or services, a cross-cutting feature, a full architectural overview): go to step 2.

When in doubt, take the simple path.

## 2. Explore (complex only)

Decompose the question into 2 to 4 angles, each a distinct slice of the subsystem. Spawn all explorers in a single message, each with `references/explorer-prompt.md` and its angle filled in.

## 3. Synthesize (complex only)

Once all explorers have returned, spawn one explainer with `references/explainer-prompt.md` and every explorer's findings filled in.

## 4. Present

Present the explainer's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.

## Output format

The explanation uses the sections defined in `references/explainer-prompt.md`, dropping any that do not apply: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.


## Related skills

- `how` (this skill) — subsystem behavior and placement
- `why` — evidence-backed rationale
- `architect` — sketch-before-code workflow that uses how/why
- `codebase-design` — deep-module vocabulary
- `architecture-patterns` — Clean / Hexagonal / DDD patterns
- `architecture-decision-records` — write the decision down
- `grilling` — stress-test a design when `interrogate` is unavailable
