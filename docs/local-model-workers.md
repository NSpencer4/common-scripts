# Local model workers

Status: Testing

Last updated: 2026-11-07

## Premise

Use a frontier model (Claude Opus) to plan, delegate, and review, and hand the hands-on work to agents running local models (opencode on Ollama). The goal is to spend fewer frontier tokens without lowering the quality of what gets merged.

The [`local-worker` skill](../skills/local-worker/SKILL.md) puts this into practice. This document holds the reasoning, the model comparison, and the trial log behind it.

## What is established

- The local stack is opencode 2.2.5 talking to Ollama at `http://127.0.0.1:11434` on an RTX 4090 (24 GB VRAM). Ollama runs as a systemd service with a 64k context.
- Installed models: `qwen3.8:27b` and `qwen3-coder:30b`.
- Claude Code drives workers non-interactively with `opencode-worker run --standalone "<task>"`, and sends corrections to the same session with `--continue`.
- With the worker setup below, `qwen3-coder:30b` completed a seven-file restructure in 39 seconds plus a 19 second correction round.

## Worker setup

The default opencode setup does not work with local models. It sends about 21,800 tokens before any work: 71,600 characters of skill descriptions (from `~/.claude/skills` and `~/.agents/skills`) and a JavaScript "Code Mode" for tool calls. On a 32k context, opencode compacts the conversation before every step, the summary drops the latest tool output, and the model repeats the same call forever.

The worker setup cuts the system prompt to about 2,300 characters (about 3,700 tokens with tool definitions):

- A separate config at `~/.config/opencode-worker/opencode/opencode.json` with only the Ollama provider, a 65,536 context limit to match Ollama, and the permissions below.
- `OPENCODE_DISABLE_CLAUDE_CODE=1`, which stops opencode from loading skills and instructions from `~/.claude`.
- Denying `skill`, which removes the remaining skill list, and `execute`, which switches off Code Mode so the model calls tools directly.
- A wrapper at `~/.local/bin/opencode-worker` that sets `XDG_CONFIG_HOME=~/.config/opencode-worker` and `OPENCODE_DISABLE_CLAUDE_CODE=1`, then runs opencode.

Pass `--standalone` so each run starts its own server with these settings instead of reusing the shared background service.

Ollama service override (`/etc/systemd/system/ollama.service.d/override.conf`), needed because the packaged unit runs as the `ollama` user with `ProtectHome=yes`:

```ini
[Service]
User=chase
Group=chase
Environment="HOME=/home/chase"
Environment="OLLAMA_MODELS=/home/chase/.ollama/models"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
Environment="OLLAMA_HOST=0.0.0.0:11434"
ProtectHome=read-only
ReadWritePaths=/home/chase/.ollama
WorkingDirectory=/home/chase/.ollama
```

## How the roles split

| Role | Model | Does |
| ---- | ----- | ---- |
| Coordinator | Frontier (Opus) | Breaks work into tasks, writes the brief, sets permissions, reviews the diff, decides what ships |
| Worker | Local (opencode + Ollama) | Reads files, edits, runs allowed commands, reports what it changed |
| Checker | Script, test, or a cheaper Claude model | Confirms the result meets the brief so the coordinator reads a pass or fail instead of the whole diff |

The coordinator never accepts a worker's report on its own; it inspects the actual changes.

## When delegation saves tokens

The frontier model still pays to write the brief and to review the result. Delegation saves tokens only when that is much smaller than doing the task directly.

| Good fit | Poor fit |
| -------- | -------- |
| Large output that is cheap to verify, such as tests for many functions, boilerplate, renames, file moves, format conversions | Small tasks where writing the brief costs as much as doing the work |
| Work with an automatic check: tests pass, linter clean, file count matches | Design decisions, subtle bugs, anything that needs judgment |
| Repeated task types that can reuse a saved brief | Work where weak output forces the coordinator to redo it |

Hidden costs: local runs are much slower, failed runs add review rounds, and loose review to save tokens lets mistakes through.

## Writing a brief for a local worker

- Name exact files, the expected end state, and what not to touch.
- One shell command per call. Chained commands (`&&`, `;`) do not match permission rules.
- Tell it not to commit or push. The coordinator commits after review.
- Ask it to finish with `git status` and a list of changes.
- A non-interactive run cannot ask questions, so the brief must answer them up front.

## Permissions

Run the worker with a scoped permission set, not with `--auto` (auto-approve everything). Claude Code's auto mode blocks `--auto` as an unsafe agent. The worker config holds this set:

```json
{
  "permission": {
    "edit": "allow",
    "webfetch": "deny",
    "external_directory": "deny",
    "shell": {
      "*": "deny",
      "mkdir -p *": "allow",
      "git mv *": "allow",
      "git status*": "allow",
      "git diff*": "allow",
      "ls": "allow",
      "ls *": "allow"
    },
    "skill": "deny",
    "execute": "deny",
    "subagent": "deny",
    "websearch": "deny",
    "question": "deny"
  }
}
```

In opencode v2 the shell permission is named `shell`, not `bash`. Allow every command the task needs, such as `mkdir -p` before `git mv` into a new folder. For a one-off change, the `OPENCODE_CONFIG_CONTENT` environment variable merges extra JSON over the config.

## Local models for a 4090

Model availability and quality change quickly. Rows marked Unverified come from model knowledge as of mid-2026 and have not been tested on this machine.

| Model | Ollama name | Use it for | Why | Downside | Status |
| ----- | ----------- | ---------- | --- | -------- | ------ |
| Qwen3 Coder 30B | `qwen3-coder:30b` | Mechanical edits, moves, renames, boilerplate | Mixture of experts with about 3B active parameters, no thinking phase, so fast | Skipped two of five brief steps on the first pass and needed a correction round | Installed, works with the worker setup (see trial log) |
| Qwen 3.8 27B | `qwen3.8:27b` | Tasks that need reasoning | Thinking model with tool support and up to 262k context | Slow: dense model plus long thinking before each action | Installed, failed only under the old setup; retest with the worker setup |
| Devstral Small 24B | `devstral` | Multi-step coding agent work | Built for coding agents such as opencode | Dense, slower than mixture of experts models | Unverified |
| gpt-oss 20B | `gpt-oss:20b` | Fast, simple tool-driven tasks | Mixture of experts with about 3.6B active parameters, around 13 GB, leaves room for large context | Weaker at writing and coding than the 24 to 30B models | Unverified |
| Mistral Small 3.2 24B | `mistral-small3.2` | General non-code tasks | Good instruction following and tool use | Not specialized for code | Unverified |

Avoid models above about 32B on 24 GB of VRAM. They spill into system RAM and run 5 to 10 times slower. Check with `ollama ps`: `PROCESSOR` should read `100% GPU`.

To add a model to opencode, add it under `provider.ollama.models` in `~/.config/opencode/opencode.json`:

```json
"qwen3-coder:30b": {
  "limit": { "context": 65536, "output": 8192 }
}
```

To compare models, give each the same small task with a known correct result and record time, retries, and how much the coordinator had to fix.

## Trial log

### 2026-11-07: restructure ideas into folders, `qwen3.8:27b`

Task, in the `NSpencer4/ideas` repository: move each `ideas/<name>.md` to `ideas/<name>/README.md` and update the root README and templates.

- Run 1 failed with no changes. Permissions used the key `bash`, so every shell command was denied. The model then hit "Compaction summary reached the output token limit" at the 32k context.
- Run 2, with the key `shell`, could run `git mv` but not `mkdir`, so every move failed with "destination directory does not exist". The model did not try another approach and the run ended with no changes.
- Result: Failed twice with no changes. Both failures came from the brief and permission setup, not only the model.

### 2026-11-07: same task, `qwen3-coder:30b`

Same brief, with `mkdir -p` allowed and an instruction to create each folder before `git mv`.

- Ran 575 seconds and made no changes.
- Read `README.md` three times and restated its plan each time without acting on it.
- Called opencode's `execute` tool to run JavaScript that listed folders. The permission set did not cover `execute`, so code execution was not blocked.
- Ended by printing a raw `<function=read>` tool call as text instead of calling the tool, a tool-call format failure.
- Result: Failed with no changes. Fast per token, but it did not follow through on a multi-step task.

Takeaways so far:

- Neither installed model completed the multi-file move task. The environment diagnosis below points to opencode setup problems, not model limits.
- The permission set must also cover the `execute` tool, not only `shell` and `edit`.

### 2026-11-07: environment diagnosis

The failures look environmental rather than a model limit.

- Opencode sends about 21,800 tokens before any work, measured with a one-line prompt and `--format json` (input plus cached tokens). With a 32,768 context and 8,192 reserved for output, about 1,700 tokens were left for the task.
- A worker config with only the Ollama provider and permissions, loaded through `XDG_CONFIG_HOME=~/.config/opencode-worker`, did not reduce that. The source of the 21,800 tokens is still unknown.
- Ollama now runs as a systemd service with `OLLAMA_CONTEXT_LENGTH=65536`, flash attention, and a q8_0 KV cache. `qwen3-coder:30b` at 64k uses 22 GB and spills 1% onto the CPU.
- At 64k context, `qwen3-coder:30b` in opencode ran `ls -la templates` 72 times without answering.
- The same tool call and result sent straight to Ollama's `/v1/chat/completions` returned the correct answer.
- A logging proxy between opencode and Ollama showed the cause. The system prompt was 81,183 characters, of which 71,591 were the `<available_skills>` list. Opencode's worker config was still at 32k, so it asked the model to summarize the conversation before the first step and again after every tool result. Each summary dropped the latest tool output, so the model repeated the call. Tool results were being sent; compaction threw them away.
- `OPENCODE_DISABLE_CLAUDE_CODE=1` cut the prompt to 28,485 characters. Denying `skill`, `execute`, `subagent`, `websearch`, and `question` cut it to 2,321 characters with no skills and no Code Mode.
- With that setup and a 65,536 context limit, the `ls` test finished in 2 seconds with one tool call and the correct answer.

### 2026-11-07: restructure ideas into folders, worker setup, `qwen3-coder:30b`

Same brief as the failed runs.

- First pass: 39 seconds. Moved all seven ideas with `git mv` without changing their content, and updated the Ideas list links. It skipped two steps: updating the README usage text and the three template references.
- Correction round with `--continue` and a list of exact lines to change: 19 seconds, all correct.
- Opus review: checked the diff, confirmed every relative link resolves, and checked for em dashes.
- Result: Completed. The earlier failures were environmental. Briefs should still be checked step by step, because the worker reported success while skipping steps.

## Questions to explore

### Does delegation save tokens on real tasks?

Context: The first trial cost more coordinator tokens in setup and diagnosis than doing the task directly.

Answer: Pending. Needs a task with large output and an automatic check.

### Can thinking be turned off for `qwen3.8:27b` through opencode?

Context: `ollama run qwen3.8:27b --think=false` works in Ollama directly. Opencode uses the OpenAI-compatible `/v1` endpoint, and passing a think-off option through it is untested.

Answer: Pending.

### Which model is best for each task type on this machine?

Context: Only `qwen3-coder:30b` has been tried with the worker setup.

Answer: Pending. Run the same task on `qwen3.8:27b`, `devstral`, and `gpt-oss:20b` with the worker setup.

### Should a cheaper Claude model do routine review?

Context: Using Sonnet or Haiku as the checker would cut frontier tokens further, keeping Opus for planning.

Answer: Pending.
