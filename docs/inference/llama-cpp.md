# llama.cpp

> Source: [github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) · also mirrored at [github.com/ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp)

## TL;DR

Pure C/C++ LLM inference engine. No Python runtime required. Runs on virtually anything: Apple Silicon (Metal), NVIDIA (CUDA), AMD (ROCm/HIP), Vulkan, and CPU. The reference implementation for GGUF models.

---

## Install

=== "macOS (Homebrew)"
    ```bash
    brew install llama.cpp
    ```

=== "Windows (winget)"
    ```bash
    winget install llama.cpp
    ```

=== "Linux / build from source"
    ```bash
    git clone https://github.com/ggerganov/llama.cpp
    cd llama.cpp
    cmake -B build -DGGML_CUDA=ON   # omit -DGGML_CUDA=ON for CPU-only
    cmake --build build --config Release -j$(nproc)
    # binaries land in build/bin/
    ```

Pre-built binaries are also available on the [GitHub releases page](https://github.com/ggerganov/llama.cpp/releases).

Models must be in **GGUF** format. Download from [Hugging Face](https://huggingface.co/models?library=gguf) or convert with `convert_hf_to_gguf.py`.

---

## llama-cli — interactive inference

```bash
llama-cli -m model.gguf                    # load and chat
llama-cli -m model.gguf -cnv               # force conversation mode
llama-cli -hf ggml-org/gemma-3-1b-it-GGUF # pull directly from HF and run
```

Key flags:

| Flag | Meaning |
|------|---------|
| `-m <path>` | Path to GGUF model file |
| `-ngl <N>` | Offload N layers to GPU (use 99 for all) |
| `-c <N>` | Context window size (tokens) |
| `-n <N>` | Max tokens to generate |
| `--threads <N>` | CPU thread count |
| `-cnv` | Enable conversation/chat mode |
| `-hf <repo>` | Download model from Hugging Face |

---

## llama-server — local HTTP server

Starts an OpenAI-compatible HTTP server (default port **8080**):

```bash
llama-server -m model.gguf --port 8080
```

Open `http://localhost:8080` in a browser for the built-in chat UI.

### LAN / network hosting

```bash
llama-server -m model.gguf --host 0.0.0.0 --port 8080
```

Key server flags:

| Flag | Meaning |
|------|---------|
| `--host <addr>` | Bind address (`0.0.0.0` for LAN) |
| `--port <N>` | Listen port (default 8080) |
| `-ngl <N>` | GPU layers to offload |
| `-c <N>` | Context window size |
| `-np <N>` | Number of parallel request slots |
| `--api-key <key>` | Require Bearer token auth |
| `--log-disable` | Suppress verbose logs |

### API endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/chat/completions` | OpenAI-compatible chat |
| `POST /v1/completions` | OpenAI-compatible completion |
| `GET  /v1/models` | List loaded model |
| `POST /v1/embeddings` | Text embeddings |
| `POST /tokenize` | Tokenise text |
| `GET  /health` | Server health check |

Example:

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama","messages":[{"role":"user","content":"Hi"}]}'
```

---

## Source code

[github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) — MIT license
