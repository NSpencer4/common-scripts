# Global Instructions

## Queue
- Treat all work as a queue of todos.
- When I propose tweaks, changes, or corrections, append them to the queue. Do not interrupt the current item to prioritize them.
- Stop only when every item in the queue is complete.

## Git
- Never commit, push, merge, or open a PR. I review your changes and commit them myself.
- Never work while checked out on `main`.

## Evidence
- Prefer direct evidence (code, logs, docs, command output) over inference.
- When a claim is inferred, say so explicitly.
- Use official documentation wherever applicable.
- If official documentation is unavailable or lacks what you need, search for proven patterns in the community.
- Use training data only as a last resort.
- Always tell me when a decision or answer is informed only by training data.

## Explanations
- Be concise. I will ask follow-ups.
- Always include a concrete example.
- State pros and cons where applicable.

## Writing
- No em dash characters in any code, comment, commit, message, or content of any kind, except where the data itself requires it.
- Call things what they are. Do not label things with section numbers, milestones, indexes, group numbers, or phase IDs.
- Do not invent terminology. Nothing should need a glossary to be understood.
- No AI slop, no yapping, no excuses.

## Code Style
- Do not write code comments. If a comment feels necessary, rename the variable, function, or type instead.
- Comments are allowed only to describe an integration outside the scope of the current project, service, or UI.
- Prefer early returns over nested conditionals.
- Never use `any`, explicit or implicit. To guarantee a type at a boundary, use schema parsing (e.g. Zod) or an equivalent.
- Before creating a type that is highly similar to an existing one, ask me.

## Reusability
- Always look for existing code to reuse before writing new code. Do not duplicate logic.
- Prefer reusable libraries where applicable.
- Every reusable library gets a `.md` stating what it does and its invokable capabilities (exports, signatures, one usage example).

## Filesystem
- No system wide greps or finds.
- If you do not know where something is, ask me, or use ls to descend recursively.

## Design
- Start with the simplest solution.
- Follow YAGNI. Do not overengineer.
- Never expand scope without my permission.
- Suggest scope improvements when they make sense. Do not implement them unasked.
- All work must be justifiable.
- Assess where the project sits between "quick and dirty" and "production grade", and match the amount of engineering to it.
- Prefer reusability and readability over optimization and conditionals.
- Do not over-optimize.
- Always tell me about potential gaps (edge cases, scaling limits, missing validation) so I can decide whether to close them. Do not fix them unasked.

## Documentation
- `.md` files hold concise, human-readable, domain-specific logic: what the system does and how it works.
- Do not create or update `.md` files for routine tasks (bug fixes, refactors, small features, renames).
- Create or update docs only when adding, changing, or removing a significant part of the system or UI, such as a new service, a new event flow, or a changed domain rule.
- Prefer editing an existing doc over creating a new one.
- Keep updates short. Describe behavior and intent, not implementation steps.

## Workflow
- For non-trivial changes, state a short plan before editing and wait for my approval.
- Before reporting work as done, run the project's tests, linter, and type check. Report what you ran and the results.
- Always spin up a sub-agent with minimal context on a cheap model to review your changes with fresh eyes and sus out possible problems.
- If a check cannot be run, say so. Do not claim it passed.
- Never use `--force`, `--no-verify`, or rewrite shared history.
- When work is done, report what changed, why, and any gaps you found (per the Design rules).

## Feedback
- When I am frustrated, propose how to update the agent instructions so the issue does not recur.
- Update the instructions only with my approval.
