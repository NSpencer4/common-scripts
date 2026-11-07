---
name: local-worker
description: Delegate a well-defined, checkable task (file moves, renames, boilerplate, mechanical edits) to a local opencode agent running on Ollama, then review and correct its work. Use when the user asks to use a local model, local agent, local subagent, opencode, or an Ollama worker, or to save frontier tokens on mechanical work. Do not use for design decisions, subtle bugs, or work that needs judgment.
---

# Local worker

You coordinate and a local model does the hands-on work. You write the brief, run the worker, review the actual diff, and send corrections. Never accept the worker's report on its own: in testing it reported success while skipping two of five steps.

Why the setup looks the way it does, with measurements from testing, is in [references/background.md](references/background.md).

## When to delegate

Delegate when the output is large but cheap to verify: moving or renaming files, boilerplate, format conversions, repetitive edits with a clear end state. Do the work yourself when writing the brief would cost about as much as the task, or when the result needs judgment to check.

## Preflight

Run these before the first worker run in a session:

```bash
command -v opencode-worker
```

```bash
curl -s -m 5 http://127.0.0.1:11434/api/tags | grep -o '"name":"[^"]*"'
```

```bash
git status --short && git branch --show-current
```

- If `opencode-worker` is missing, recreate it from [setup/](setup/) as described in [setup/README.md](setup/README.md). Ask the user before writing files outside the repository.
- If Ollama does not answer, check `systemctl status ollama --no-pager`. Starting or reconfiguring the service needs sudo, so tell the user what to run.
- Work on a feature branch with a clean tree, so the worker's changes are the whole diff.

## Write the brief

Write the brief to a file in your scratchpad. A non-interactive run cannot ask questions, so answer them in the brief.

- Name every file to change, the expected end state, and what must not change.
- Number the steps. You will check each one.
- Shell rules: one command per call, never chain with `&&` or `;`, never `cd`. Name the only commands allowed. Chained commands do not match permission rules and are denied.
- If a command needs a folder that does not exist, say to run `mkdir -p` first.
- Tell it not to commit or push. You commit after review.
- Ask it to finish with `git status` and a short list of changes.
- Repeat any repository writing rules the result must follow, such as banned characters.

## Permissions

The worker config allows file edits, denies everything outside the working directory, and allows only `mkdir -p`, `git mv`, `git status`, `git diff`, and `ls` in the shell. It denies `skill`, `execute`, `subagent`, `websearch`, `question`, and `webfetch`.

If a task needs another command, add it for that run only:

```bash
OPENCODE_CONFIG_CONTENT='{"permission":{"shell":{"git rm *":"allow"}}}' opencode-worker run --standalone "..."
```

Never pass `--auto`. It approves every action, and Claude Code's auto mode blocks it as an unsafe agent. Never allow `"*"` in `shell`. Keep `execute` denied: it lets the model run arbitrary JavaScript and switches on a code-mode tool format that local models handle poorly.

## Run

Run from the repository root, in the background, with a timeout:

```bash
START=$(date +%s); timeout 1200 opencode-worker run --standalone --title "<short title>" "$(cat <scratchpad>/brief.md)" > <scratchpad>/worker.log 2>&1; echo "exit=$? seconds=$(( $(date +%s) - START ))" >> <scratchpad>/worker.log
```

- `--standalone` starts a private server that uses the worker config. Without it, opencode connects to a shared background service that may have been started with other settings.
- The default model is `ollama/qwen3-coder:30b`, which is fast and has handled mechanical tasks. For a task that needs more reasoning, add `--model ollama/qwen3.8:27b`, which is much slower and has not yet been tested with this setup.
- Wait for the completion notice instead of polling the log.

## Review

1. Read the end of the log, then `git status --short` and `git diff -M HEAD --stat`.
2. Check each numbered step of the brief against the diff. Skipped steps are the most common failure.
3. Run whatever check fits the task: tests, a linter, a link check, a search for leftover old paths.
4. Check for content the worker should not have changed. A move should show as a 100% rename.

## Correct

Send corrections to the same session so the worker keeps its context:

```bash
timeout 600 opencode-worker run --standalone --continue "$(cat <scratchpad>/fix.md)" > <scratchpad>/worker-fix.log 2>&1
```

- Say what is already correct, then list each fix with the exact file and line, and the exact replacement where possible.
- `--continue` resumes the most recent session. If another worker ran since, use `--session <id>` with the `sessionID` from that run's output (add `--format json` to the run to get it).
- Review again after every round. After two failed rounds on the same step, do that step yourself and record why.

## Commit and record

- Commit the worker's change on its own, with a message that says a local worker did it and you reviewed it.
- In your final response, report the model, seconds per round, what the worker skipped or got wrong, and the result. If the user keeps a log of local worker trials, add a dated entry there too.

## Troubleshooting

| Symptom | Likely cause | What to do |
| ------- | ------------ | ---------- |
| The same tool call repeats and the model never answers | The prompt is too big for the context, so opencode compacts before every step and drops the tool output | Measure the starting prompt (below). It should be about 4,000 tokens. If it is much higher, check that `--standalone` was used and the run went through `opencode-worker` |
| `Permission denied: shell` on an allowed command | The command was chained, or the rule key is wrong | One command per call. In opencode v2 the key is `shell`, not `bash` |
| The model prints `<function=...>` text instead of calling a tool | Tool-call format failure, often with code mode on | Confirm `execute` is denied in the worker config |
| `ECONNREFUSED` | Ollama is not running | `systemctl status ollama --no-pager` and ask the user to start it |
| Very slow responses | The model spilled out of VRAM | `ollama ps` should show `100% GPU`. Close other GPU users or lower `OLLAMA_CONTEXT_LENGTH` |
| `Compaction summary reached the output token limit` | Context overflow | Same as the first row |

Measure the starting prompt:

```bash
opencode-worker run --standalone --format json "Reply with the word ok and nothing else." | grep -o '"tokens":{[^}]*}[^}]*}'
```

The real size is `input` plus `cache.read`.

## Process cleanup

`--standalone` runs exit on their own. To stop a stuck worker, find its process ID with `pgrep -af "opencode run"` and `kill` that ID. Do not use `pkill -f` with a pattern that also appears in your own command, because it kills your own shell. Leave `opencode acp` and `opencode serve --stdio` processes alone; the user's editor owns them.
