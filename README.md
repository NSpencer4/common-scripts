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
