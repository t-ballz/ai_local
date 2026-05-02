# LM Studio

> Source: [lmstudio.ai](https://lmstudio.ai) · CLI source: [github.com/lmstudio-ai/lms](https://github.com/lmstudio-ai/lms)

## TL;DR

Desktop app + headless server for running local models. Provides a GUI for browsing and downloading models, and an OpenAI-compatible REST API on port **1234**. The `lms` CLI controls everything from the terminal. The app itself is closed-source; the CLI SDK is MIT-licensed.

---

## Install

=== "macOS / Linux"
    ```bash
    curl -fsSL https://lmstudio.ai/install.sh | bash
    ```

=== "Windows (PowerShell)"
    ```powershell
    irm https://lmstudio.ai/install.ps1 | iex
    ```

The installer places the `lms` CLI in your PATH. Verify:

```bash
lms --help
```

---

## Basic CLI commands (`lms`)

```bash
lms get qwen3-4b          # search and download a model
lms ls                    # list models on disk
lms load qwen3-4b         # load a model into memory
lms ps                    # show currently loaded models
lms chat                  # interactive terminal chat (uses loaded model)
lms unload --all          # unload all models from memory
lms import /path/to/model.gguf  # import an external GGUF file
```

Load options:

```bash
lms load qwen3-4b --gpu max              # full GPU offload
lms load qwen3-4b --gpu 0.5            # 50% GPU offload
lms load qwen3-4b --context-length=8192
lms load qwen3-4b --identifier="mymodel"  # custom API name
```

---

## Running the server

```bash
lms server start          # start on default port 1234
lms server stop
lms server status
lms log stream            # tail server logs
```

### Headless / daemon mode (no GUI)

```bash
lms daemon up             # start headless background daemon
lms daemon down
lms daemon status
```

This is the recommended mode for Linux servers and CI environments.

### LAN / network hosting

LM Studio's server binds to `localhost:1234` by default. To expose it on the local network:

```bash
lms server start --bind 0.0.0.0 --port 1234
```

---

## REST API

Base URL: `http://localhost:1234` · OpenAI-compatible

| Endpoint | Purpose |
|----------|---------|
| `GET  /v1/models` | List loaded models |
| `POST /v1/chat/completions` | Chat (streaming supported) |
| `POST /v1/completions` | Text completion |
| `POST /v1/embeddings` | Embeddings |

SDKs:

```bash
pip install lmstudio        # Python
npm install @lmstudio/sdk   # JavaScript/TypeScript
```

---

## Source code

- **App**: closed-source
- **CLI / SDK**: [github.com/lmstudio-ai/lms](https://github.com/lmstudio-ai/lms) — MIT license
