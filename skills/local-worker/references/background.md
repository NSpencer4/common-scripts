# Background

Findings from testing opencode 2.2.5 with Ollama on an RTX 4090 (24 GB) on 2026-11-07. They explain each part of the worker setup.

## Why a separate worker config

With the default opencode setup, a one-line prompt sent about 21,800 tokens. A logging proxy between opencode and Ollama showed the system prompt was 81,183 characters, of which 71,591 were an `<available_skills>` list built from `~/.claude/skills` and `~/.agents/skills`.

When that prompt does not fit comfortably in the configured context, opencode asks the model to summarize the conversation before the first step and again after every tool result. Each summary drops the latest tool output, so the model repeats the same tool call indefinitely. In one run, the model ran `ls -la templates` 72 times without answering. Sending the same tool call and result straight to Ollama returned the correct answer, which ruled out the model and Ollama.

| Setup | System prompt characters | Skills listed |
| ----- | ------------------------ | ------------- |
| Default | 79,382 | 107 |
| `OPENCODE_DISABLE_CLAUDE_CODE=1` | 28,485 | 32 |
| Plus `skill`, `execute`, `subagent`, `websearch`, `question` denied | 2,321 | 0 |

With the last setup the starting prompt is about 3,650 tokens, including tool definitions.

## Why `execute` is denied

Opencode v2 has a code mode in which tools are called through JavaScript run by an `execute` tool. Local models handled it poorly: `qwen3-coder:30b` printed raw `<function=...>` text instead of calling tools. `execute` also runs arbitrary code, which the shell permission rules do not cover. Denying it removes code mode, and the model calls tools directly.

## Why `--standalone`

`opencode run` normally connects to a shared background service that another tool or an earlier run may have started with different settings. Whether that service picks up a later run's `XDG_CONFIG_HOME` has not been tested. `--standalone` starts a private server for the run, so the worker settings are known to apply; all of the results below used it.

## Why one command per call

Permission rules match the whole command string. `git status && git branch` matches neither `git status*` nor anything else, so it is denied. In opencode v2 the shell permission key is `shell`, not `bash`.

## Results with the worker setup

| Task | Model | Result |
| ---- | ----- | ------ |
| `ls templates` and count the files | `qwen3-coder:30b` | 2 seconds, one tool call, correct |
| Move seven Markdown files into folders and update a README and three templates | `qwen3-coder:30b` | 39 seconds; moves correct, but skipped two of five brief steps while reporting success. One correction round with exact lines fixed both in 19 seconds |

`qwen3.8:27b` failed only under the old setup and has not been retested with the worker setup.

## Token economics

The coordinator still pays to write the brief and review the result. Delegation saves tokens only when the worker's output is much larger than the brief and review, and cheap to check: tests passing, a link check, a diff of renames. For small tasks, briefing and reviewing can cost as much as doing the work.
