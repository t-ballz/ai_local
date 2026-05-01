# Ollama

> Source: [ollama.com](https://ollama.com) · [github.com/ollama/ollama](https://github.com/ollama/ollama)

## TL;DR

The simplest way to run open models locally. One-line install, pull-and-run workflow, built-in OpenAI-compatible REST API on port 11434. Written in Go.

---

## Install

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

On macOS you can also download the `.app` from [ollama.com](https://ollama.com). The app registers `ollama` in your PATH and starts a background service automatically.

---

## Basic commands

```bash
ollama pull llama3.2          # download a model
ollama run llama3.2           # interactive chat (pulls if not present)
ollama run llama3.2 "prompt"  # one-shot, non-interactive
ollama list                   # show downloaded models
ollama show llama3.2          # model metadata, parameters, template
ollama rm llama3.2            # delete a model
ollama cp llama3.2 my-llama   # copy/rename
ollama serve                  # start server manually (auto-starts on install)
```

Pass model options inline:

```bash
ollama run llama3.2 --verbose        # show token stats
ollama run llama3.2 /set num_ctx 8192  # set context length for this session
```

---

## Running the server

Ollama starts as a background service after install. To control it manually:

```bash
ollama serve                  # foreground, logs to stdout
systemctl status ollama       # on Linux (installed via script)
```

### LAN / network hosting

By default Ollama binds to `127.0.0.1:11434`. To expose it on your local network:

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

Or set it permanently in the systemd service (`/etc/systemd/system/ollama.service`):

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

---

## REST API

Default base URL: `http://localhost:11434`

| Endpoint | Purpose |
|----------|---------|
| `POST /api/generate` | Single-turn text completion |
| `POST /api/chat` | Multi-turn chat (messages array) |
| `GET /api/tags` | List downloaded models |
| `POST /api/pull` | Download a model |
| `DELETE /api/delete` | Remove a model |

OpenAI-compatible endpoints (drop-in replacement):

```
POST /v1/chat/completions
POST /v1/completions
GET  /v1/models
```

Example:

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'
```

---

## Source code

[github.com/ollama/ollama](https://github.com/ollama/ollama) — MIT license, ~171K stars (2026-05-02)
