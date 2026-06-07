# turbovec — Vector Index for Local RAG

> Source: [MarkTechPost](https://www.marktechpost.com/2026/05/20/meet-turbovec-a-rust-vector-index-with-python-bindings-and-built-on-googles-turboquant-algorithm/) · [ICLR 2026 TurboQuant paper]

## TL;DR

A Rust vector search library with Python bindings that implements Google's [TurboQuant](../inference/turboquant.md) for embedding compression. Stores vectors at 2–4 bits/dimension with zero training data required — 10M vectors in ~4 GB instead of ~60 GB (float32). Faster than FAISS IndexPQFastScan on ARM hardware.

---

## The problem it solves

Standard vector stores keep embeddings in float32 or float16. For large corpora this is expensive:

| Corpus | float32 | turbovec 4-bit |
|--------|---------|---------------|
| 100K docs | ~600 MB | ~50 MB |
| 1M docs | ~6 GB | ~400 MB |
| 10M docs | ~60 GB | **~4 GB** |

turbovec uses **TurboQuant** — a data-oblivious quantizer that compresses to 2–4 bits/dimension without any training, codebook calibration, or rebuilds when the corpus changes.

---

## Key properties

| Property | Value |
|----------|-------|
| Implementation | Rust + PyO3 (Python bindings) |
| Compression | 2–4 bits/dimension (TurboQuant) |
| Training required | None |
| Rebuild on corpus update | None |
| Search vs FAISS IndexPQFastScan (ARM) | 12–20% faster |
| Recall@1 (4-bit, 100K DBpedia vectors) | 0.955 |
| Query latency (4-bit, Apple M3 Max) | 0.232 ms |

---

## Install & quickstart

```bash
pip install turbovec
```

```python
import turbovec
import numpy as np

# Create index — no training step
index = turbovec.Index(dim=1536, bits=4)

# Add vectors
vecs = np.random.randn(10_000, 1536).astype(np.float32)
index.add(vecs)

# Search
query = np.random.randn(1536).astype(np.float32)
ids, distances = index.search(query, k=10)
```

---

## Local RAG use case

turbovec pairs well with llama.cpp or Ollama for private, memory-constrained RAG:

- No network calls or server process
- Multi-million-document corpora fit on a laptop
- Instantly update the corpus — no index rebuilds

See also: [TurboQuant](../inference/turboquant.md) — the same compression algorithm applied to live KV cache in LLM inference.
