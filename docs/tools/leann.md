# LEANN: Low-Storage Vector Index

> Source: [arXiv:2506.08276](https://arxiv.org/abs/2506.08276) · MLSys 2026  
> GitHub: [yichuan-w/LEANN](https://github.com/yichuan-w/LEANN)

## TL;DR

LEANN is a vector index that achieves **97% storage savings** compared to traditional approaches by recomputing embeddings on-the-fly during search rather than persisting them. Designed specifically for personal devices — laptops included — it indexes millions of documents in a few hundred MB while maintaining SOTA recall and comparable query latency.

---

## The problem with traditional vector DBs

Standard vector databases (FAISS, HNSW-based systems) store every document embedding alongside the index graph. For large corpora this means:

- A 60M-document Wikipedia index: **201 GB**
- A 2.1M-document DPR dataset: **3.8 GB**

The storage cost scales linearly with the number of documents and the embedding dimension, and the index often exceeds the size of the original corpus.

---

## How LEANN works

Two complementary techniques:

### 1. On-the-fly recomputation

Instead of storing embeddings, LEANN stores only the original source text (or a pointer to it). During a search traversal of the proximity graph, embeddings are **recomputed on demand** for only the nodes actually visited — typically a tiny fraction of the full corpus.

The bet is that graph-guided traversal visits far fewer nodes than brute-force search, making recomputation cost acceptable.

### 2. High-degree preserving pruning

The proximity graph itself (HNSW or DiskANN) is pruned to compress storage, but the pruning is not uniform. **High-degree nodes** (hubs with many connections) are preserved because they dominate search traversal — losing them collapses recall. Low-degree peripheral nodes are pruned more aggressively.

The result is a **CSR-format compressed graph** that maintains search quality with a fraction of the storage.

---

## Storage benchmarks

| Corpus | Docs | Traditional DB | LEANN | Savings |
|--------|------|---------------|-------|---------|
| DPR | 2.1M | 3.8 GB | 324 MB | 91% |
| Wikipedia | 60M | 201 GB | 6 GB | 97% |
| Chat history | 400K | 1.8 GB | 64 MB | 97% |
| Email | 780K | 2.4 GB | 79 MB | 97% |
| Browser history | 38K | 130 MB | 6.4 MB | 95% |

Accuracy: SOTA recall maintained. Latency: comparable to stored-embedding approaches for RAG workloads.

---

## Installation

Requires [`uv`](https://astral.sh/uv):

```bash
git clone https://github.com/yichuan-w/LEANN.git leann
cd leann
uv venv && source .venv/bin/activate
uv pip install leann
```

Platform-specific system dependencies required for the DiskANN backend:
- **macOS 13.3+**: `brew install libomp boost protobuf zeromq pkgconf`
- **Ubuntu/Debian**: build tools + Intel MKL
- **Windows**: Visual Studio 2022 + vcpkg

---

## Usage

### CLI

```bash
leann build myindex --docs ./documents/
leann search myindex "how does transformer attention work"
leann ask myindex --interactive
```

### Python API

```python
from leann import LeannBuilder, LeannSearcher

builder = LeannBuilder(backend_name="hnsw")
builder.add_text("Your content here")
builder.build_index("path/to/index")

searcher = LeannSearcher("path/to/index")
results = searcher.search("query", top_k=5)
```

---

## Embedding model support

LEANN uses an **OpenAI-compatible API** for embeddings — any local or cloud provider works:

| Type | Compatible providers |
|------|---------------------|
| Local | Ollama, LM Studio, llama.cpp, vLLM, SGLang |
| Cloud | OpenAI, DeepSeek, Mistral, Anthropic, Gemini, Groq |

Default model: `facebook/contriever`. Override with `--embedding-model`.

```bash
export OPENAI_BASE_URL=http://localhost:11434/v1  # point at Ollama
export OPENAI_API_KEY=ollama
leann build myindex --docs ./docs --embedding-model nomic-embed-text
```

---

## MCP integration

LEANN ships a native MCP server, making it a drop-in semantic search backend for Claude Code and other MCP-compatible clients. Prebuilt connectors exist for Slack and Twitter bookmarks; the framework is extensible.

---

## Limitations

- DiskANN backend requires macOS 13.3+ or a supported Linux distro with MKL
- Recomputation adds latency per query hop — acceptable for RAG but may matter for high-QPS serving
- No documented GPU requirement (CPU-only by default)
- iMessage/email connectors are macOS-only initially

---

## Source

- **Paper**: [arXiv:2506.08276](https://arxiv.org/abs/2506.08276) — MLSys 2026
- **GitHub**: [yichuan-w/LEANN](https://github.com/yichuan-w/LEANN)
