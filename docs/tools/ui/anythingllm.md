# AnythingLLM

> Source: [anythingllm.com](https://anythingllm.com) · [github.com/Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm)

## TL;DR

Full-stack, privacy-first AI platform. Think: ChatGPT-style UI + RAG + agent tools, running entirely on your hardware with no account needed. Sits *on top of* inference backends (Ollama, llama.cpp, LM Studio, etc.) rather than running models itself. MIT-licensed.

!!! note "This is a UI layer, not an inference engine"
    AnythingLLM needs a separate model backend (Ollama, LM Studio, llama.cpp server, or a cloud API). Configure it under **Settings → LLM Provider**.

---

## Install

### Desktop app (simplest)

One-click installer for macOS, Windows, and Linux — available at [anythingllm.com](https://anythingllm.com). No Docker or terminal required.

### Docker (recommended for LAN / self-hosted)

```bash
docker run -d \
  -p 3001:3001 \
  --cap-add SYS_ADMIN \
  -v ${HOME}/anythingllm:/app/server/storage \
  --name anythingllm \
  mintplexlabs/anythingllm
```

Then open `http://localhost:3001`.

Key options:

| Flag | Purpose |
|------|---------|
| `-p 3001:3001` | Expose UI on port 3001 |
| `--cap-add SYS_ADMIN` | Required for Chromium-based document parsing |
| `-v .../storage` | Persist uploaded docs, vector DB, and settings |

### LAN access

The Docker container listens on all interfaces by default. Anyone on your network can reach it at `http://<your-ip>:3001`. Enable multi-user mode and set passwords under **Settings → Multi-User Mode** before exposing it broadly.

---

## docker-compose

```yaml
services:
  anythingllm:
    image: mintplexlabs/anythingllm
    container_name: anythingllm
    ports:
      - "3001:3001"
    cap_add:
      - SYS_ADMIN
    volumes:
      - ./storage:/app/server/storage
    restart: unless-stopped
```

---

## Supported LLM backends

40+ providers, including:

- **Local**: Ollama, LM Studio, llama.cpp server, LocalAI
- **Cloud**: OpenAI, Azure OpenAI, Anthropic, Google Gemini, Mistral, Groq, DeepSeek, and many more

---

## Key features

- Chat with documents (PDF, Word, CSV, code, web pages)
- RAG with pluggable vector DBs (LanceDB default, Chroma, Qdrant, Pinecone, Weaviate, etc.)
- AI agents with web browsing, code execution, and custom tools
- Multi-user support with permissions
- Full developer REST API (`/api/...`)
- Browser extension + embeddable web widget

---

## Source code

[github.com/Mintplex-Labs/anything-llm](https://github.com/Mintplex-Labs/anything-llm) — MIT license
