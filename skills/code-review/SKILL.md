---
name: code-review
description: >-
  Review changes since a fixed point (commit, branch, tag, or merge-base) on two
  axes: Standards (repo coding standards) and Spec (originating issue/spec).
  Runs both reviews in parallel sub-agents and reports them side by side. Use
  when reviewing a branch, a PR, WIP changes, or "review since X". Uses GitHub
  via the gh CLI for issue/PR context.
---

# Code Review

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** with fresh context, then this skill
aggregates their findings.

Prefer **GitHub + `gh`** for issue and PR context. Do not invent a separate
tracker setup skill.

## Process

### 1. Pin the fixed point

Whatever the user named (commit SHA, branch, tag, `main`, `HEAD~5`, etc.). If
missing, ask.

Capture once:

- Diff: `git diff <fixed-point>...HEAD` (three-dot / merge-base)
- Commits: `git log <fixed-point>..HEAD --oneline`

Confirm the ref resolves (`git rev-parse <fixed-point>`) and the diff is
non-empty before spawning sub-agents.

### 2. Identify the spec source

Look in this order:

1. Issue or PR references in commits (`#123`, `Closes #45`, etc.). Fetch with:
   - `gh issue view <n> --json title,body,labels,state`
   - or `gh pr view <n> --json title,body,closingIssuesReferences,commits`
   - If reviewing the current branch's PR: `gh pr view --json number,title,body,closingIssuesReferences`
2. A path the user passed as an argument
3. A spec under `docs/`, `specs/`, or `.scratch/` matching branch/feature
4. If nothing is found, ask. If there is no spec, the Spec axis reports "no spec available"

### 3. Identify the standards sources

Search the repo for how code should be written. When `CODING_STANDARDS.md`,
`CONTRIBUTING.md`, `AGENTS.md`, or package/agent instruction files exist, include
them.

On top of repo docs, always carry the **smell baseline** below (Fowler,
_Refactoring_ ch.3). Rules:

- **The repo overrides.** Documented standards win over the baseline.
- **Always a judgement call** for baseline smells. Skip anything tooling already enforces.

Smell → fix direction:

- **Mysterious Name** → rename; if no honest name comes, the design is murky
- **Duplicated Code** → extract the shared shape
- **Feature Envy** → move behavior onto the data it envies
- **Data Clumps** → bundle travelling fields into one type
- **Primitive Obsession** → give the domain concept its own type
- **Repeated Switches** → polymorphism or one shared map
- **Shotgun Surgery** → gather what changes together
- **Divergent Change** → split so each module changes for one reason
- **Speculative Generality** → delete unused abstraction
- **Message Chains** → hide the walk behind one method
- **Middle Man** → cut the pass-through
- **Refused Bequest** → prefer composition

### 4. Spawn both sub-agents in parallel

**Standards** prompt includes: diff command, commit list, standards file paths,
the smell baseline pasted in full, and: report documented-standard breaches
(cite file + rule) and baseline smells (name + hunk). Distinguish hard
violations from judgement calls. Under 400 words.

**Spec** prompt includes: diff command, commit list, issue/PR/spec text, and:
missing/partial requirements, unrequested scope creep, wrong-looking
implementations — quote the spec/issue line for each. Under 400 words.

Skip Spec if no spec source exists.

### 5. Aggregate

Present under `## Standards` and `## Spec` separately. Do not merge or rerank
across axes. End with counts per axis and the worst issue within each axis.

## Why two axes

Standards-clean code can still implement the wrong thing. Spec-faithful code can
still break project conventions. Keep the axes separate so one cannot mask the
other.

## Review craft

After the Standards/Spec axes, or when the user asks how to give better review feedback (not just what to check), use:

- [review-craft.md](references/review-craft.md)
- [review-patterns.md](references/review-patterns.md)
- [review-techniques.md](references/review-techniques.md)

The `gh`-based process and two-axis structure above still own workflow and report shape.
