#!/usr/bin/env bash
# Idempotent linker: point local AI tool global paths at this repo.
# Usage: ./scripts/link-ai-globals.sh
# Optional: REPO_ROOT=/path/to/common-scripts ./scripts/link-ai-globals.sh

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
BACKUP_ROOT="${BACKUP_ROOT:-$HOME/.ai-globals-backup-$(date +%Y%m%d-%H%M%S)}"

backup_and_link() {
  local target="$1"
  local source="$2"
  if [[ -L "$target" ]]; then
    local current
    current=$(readlink "$target")
    if [[ "$current" == "$source" ]]; then
      echo "ok  $target"
      return 0
    fi
  fi
  if [[ -e "$target" || -L "$target" ]]; then
    local parent base
    parent=$(dirname "$target")
    base=$(basename "$target")
    mkdir -p "$BACKUP_ROOT$parent"
    mv "$target" "$BACKUP_ROOT$parent/$base"
    echo "bak $target -> $BACKUP_ROOT$parent/$base"
  fi
  mkdir -p "$(dirname "$target")"
  ln -s "$source" "$target"
  echo "lnk $target -> $source"
}

echo "REPO_ROOT=$REPO_ROOT"

test -f "$REPO_ROOT/AGENTS-GLOBAL.md"
test -d "$REPO_ROOT/skills"
test -f "$REPO_ROOT/cursor/rules/global.mdc"

backup_and_link "$HOME/.cursor/skills" "$REPO_ROOT/skills"
backup_and_link "$HOME/.claude/skills" "$REPO_ROOT/skills"
backup_and_link "$HOME/.codex/skills" "$REPO_ROOT/skills"
backup_and_link "$HOME/.config/opencode/skills" "$REPO_ROOT/skills"
backup_and_link "$HOME/.junie/skills" "$REPO_ROOT/skills"

backup_and_link "$HOME/.claude/AGENTS.md" "$REPO_ROOT/AGENTS-GLOBAL.md"
backup_and_link "$HOME/.codex/AGENTS.md" "$REPO_ROOT/AGENTS-GLOBAL.md"
backup_and_link "$HOME/.config/opencode/AGENTS.md" "$REPO_ROOT/AGENTS-GLOBAL.md"
backup_and_link "$HOME/.junie/AGENTS.md" "$REPO_ROOT/AGENTS-GLOBAL.md"
backup_and_link "$HOME/.cursor/rules/global.mdc" "$REPO_ROOT/cursor/rules/global.mdc"

# Claude alias file: relative link next to AGENTS.md
if [[ -L "$HOME/.claude/CLAUDE.md" || -e "$HOME/.claude/CLAUDE.md" ]]; then
  if [[ "$(readlink "$HOME/.claude/CLAUDE.md" 2>/dev/null || true)" != "AGENTS.md" ]]; then
    mkdir -p "$BACKUP_ROOT$HOME/.claude"
    mv "$HOME/.claude/CLAUDE.md" "$BACKUP_ROOT$HOME/.claude/CLAUDE.md"
    ln -s AGENTS.md "$HOME/.claude/CLAUDE.md"
    echo "lnk $HOME/.claude/CLAUDE.md -> AGENTS.md"
  else
    echo "ok  $HOME/.claude/CLAUDE.md"
  fi
else
  ln -s AGENTS.md "$HOME/.claude/CLAUDE.md"
  echo "lnk $HOME/.claude/CLAUDE.md -> AGENTS.md"
fi

echo "Done. Backups (if any): $BACKUP_ROOT"
