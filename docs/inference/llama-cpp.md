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

## MoE and CPU/GPU split inference

For large MoE models that exceed VRAM, llama.cpp can automatically split across GPU and RAM. The recommended approach — keeping attention/KV in VRAM and offloading routed expert weights to RAM — is controlled with a handful of flags.

### Key flags

| Flag | Meaning |
|------|---------|
| `--fit on` | Auto-fit model across available GPU VRAM and system RAM (MoE-aware) |
| `-ngl 99` | Send all layers to GPU first (combine with `--fit` or `--n-cpu-moe`) |
| `--n-cpu-moe` | Move routed expert weights back to RAM after `-ngl 99` |
| `-fa on` | Enable flash attention — faster KV operations (**requires CUDA ≥ 8.0 / Volta+, not Pascal**) |
| `-ctk q8_0` | Quantise the K-cache to 8-bit — saves VRAM with minimal quality loss |
| `-ctv q8_0` | Quantise the V-cache to 8-bit — same |
| `--no-context-shift` | Disable automatic context sliding/trimming when the window fills |
| `--chat-template-kwargs` | Pass JSON options to the chat template (see thinking mode below) |

### Practical example: Qwen3.6-35B-A3B on a hybrid setup

This command was shared by the community as a reference for running a 35B MoE model across GPU VRAM and system RAM:

```bash
llama-server \
    --model ~/models/Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf \
    --port 8001 \
    --alias qwen3.6-35b-a3b \
    -c 131072 \
    -n 32768 \
    --no-context-shift \
    --temp 0.6 \
    --top-p 0.95 \
    --top-k 20 \
    --repeat-penalty 1.00 \
    --presence-penalty 0.00 \
    --fit on \
    -fa on \
    -ctk q8_0 \
    -ctv q8_0 \
    --chat-template-kwargs '{"preserve_thinking": true}'
```

What each flag does:

| Flag | Effect |
|------|--------|
| `-c 131072` | 128K context window (131072 = 128 × 1024) |
| `-n 32768` | Up to 32K output tokens |
| `--no-context-shift` | Don't slide/trim old context when the window fills |
| `--temp 0.6` | Moderate randomness |
| `--top-p 0.95` | Sample from top 95% probability mass |
| `--top-k 20` | Consider only the top 20 next-token candidates |
| `--repeat-penalty 1.00` | No extra repetition penalty |
| `--presence-penalty 0.00` | No presence penalty |
| `--fit on` | Auto-split model across VRAM and RAM |
| `-fa on` | Flash attention (Volta+ GPU only) |
| `-ctk q8_0` | K-cache stored at 8-bit |
| `-ctv q8_0` | V-cache stored at 8-bit |
| `--chat-template-kwargs '{"preserve_thinking": true}'` | Keep `<think>` blocks visible in output |

!!! note "Model filename decoded"
    `Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf`:  
    **Qwen3.6** = model family · **35B** = total params · **A3B** = ~3B active per token (MoE) · **UD** = Unsloth Dynamic quantization · **Q4_K_XL** = 4-bit, larger/higher-fidelity variant than Q4_K_M

!!! warning "Flash attention compatibility"
    `-fa on` requires CUDA ≥ 8.0 (Volta, Turing, Ampere, Ada, Hopper). It will not work on Pascal (GTX 1050 Ti, GTX 10xx series, CUDA 6.1). Omit `-fa on` on Pascal hardware.

!!! tip "KV cache quantisation"
    `-ctk q8_0 -ctv q8_0` reduces KV cache VRAM usage significantly at long contexts with negligible quality impact. Use this whenever VRAM is tight, regardless of whether you are running MoE or dense models.

---

## Source code

[github.com/ggerganov/llama.cpp](https://github.com/ggerganov/llama.cpp) — MIT license
