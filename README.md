# AI Local — Personal Knowledge Base

**https://t-ballz.github.io/ai_local/**

A personal wiki on running AI locally — models, inference engines, tools, and research worth understanding. Built with MkDocs Material and deployed to GitHub Pages.

## What's in it

| Section | Contents |
|---------|----------|
| **Hardware** | Build notes for specific rigs (Ryzen 7 9700X + RTX 5060, i5-4570 + GTX 1050 Ti) |
| **Models** | Open-weight model families: Llama, Qwen, DeepSeek, Gemma, Mistral, Kimi, Nemotron, Nex N2, and more; plus specialised models (ASR, TTS, embedding, image gen) |
| **Inference** | Ollama, llama.cpp, LM Studio, quantisation/KV cache techniques |
| **Tips** | Agentic AI engineering patterns, loop engineering |
| **Research** | Papers on training methods, agent architectures, attention efficiency, and reasoning |
| **Tools** | UI frontends, CLI agents, vector search (LEANN, turbovec, Zvec), code intelligence (codebase-memory-mcp) |
| **Software Thoughts** | Foundational software concepts worth keeping (distributed systems, engineering patterns) |

## Running locally

```bash
make install   # create .venv and install deps
make serve     # live-reload dev server at http://localhost:8000
make build     # static build (--strict)
make deploy    # push to GitHub Pages
```

Requires Python 3.10+. The shared `.venv/` covers both MkDocs and the digest inbox tools.

## Digest inbox

`inbox/` is a daily digest system that enumerates new items from configured sources (HuggingFace papers, Simon Willison's blog, r/LocalLLaMA, HuggingFace blog) and presents them for wiki intake. Run via `/project:digest` inside Claude Code, or directly:

```bash
.venv/bin/python inbox/run_digest.py
```

Digests are written to `inbox/digests/` (gitignored).
