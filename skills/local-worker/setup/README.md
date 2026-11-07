# Local worker setup

These files recreate the `opencode-worker` command that the local worker skill uses.

| File | Install to | Purpose |
| ---- | ---------- | ------- |
| `opencode.json` | `~/.config/opencode-worker/opencode/opencode.json` | Ollama provider, default model `qwen3-coder:30b`, 65,536 context, scoped permissions, skills and code mode denied |
| `opencode-worker` | `~/.local/bin/opencode-worker` (executable) | Runs opencode with `XDG_CONFIG_HOME` pointed at the worker config and `OPENCODE_DISABLE_CLAUDE_CODE=1` so no skills or `~/.claude` instructions load |

```bash
mkdir -p ~/.config/opencode-worker/opencode
```

```bash
cp ~/.claude/skills/local-worker/setup/opencode.json ~/.config/opencode-worker/opencode/opencode.json
```

```bash
install -m 755 ~/.claude/skills/local-worker/setup/opencode-worker ~/.local/bin/opencode-worker
```

Requirements:

- `opencode` 2.x on the `PATH`.
- Ollama serving `qwen3-coder:30b` at `http://localhost:11434` with a context length of at least 65,536.

The context limit in `opencode.json` must not exceed what Ollama serves. If it is lower than the starting prompt plus room for work, opencode compacts before every step and the worker loops.

## Ollama as a systemd service

Running Ollama through systemd keeps its settings fixed and sends its logs to `journalctl -u ollama`. The packaged unit runs as the `ollama` user with `ProtectHome=yes`, so it cannot see models under a home folder. This override in `/etc/systemd/system/ollama.service.d/override.conf` runs it as your user instead. Replace `<user>` with your username.

```ini
[Service]
User=<user>
Group=<user>
Environment="HOME=/home/<user>"
Environment="OLLAMA_MODELS=/home/<user>/.ollama/models"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
Environment="OLLAMA_CONTEXT_LENGTH=65536"
Environment="OLLAMA_HOST=0.0.0.0:11434"
ProtectHome=read-only
ReadWritePaths=/home/<user>/.ollama
WorkingDirectory=/home/<user>/.ollama
```

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl enable --now ollama
```

Flash attention and the q8_0 KV cache roughly halve the memory a 64k context needs. On a 24 GB GPU, `qwen3-coder:30b` at 64k then uses about 22 GB. Check with `ollama ps` that `PROCESSOR` reads `100% GPU` or close to it.
