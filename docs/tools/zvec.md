# Zvec

> Source: [github.com/alibaba/zvec](https://github.com/alibaba/zvec) · [zvec.org](https://zvec.org) · February 2026  
> Apache 2.0 · `pip install zvec`

## TL;DR

Alibaba's **embedded, in-process vector database** — the SQLite of vector DBs. No server, no daemon, no config: it runs as a library inside your application. Built on Proxima, Alibaba's internal production vector engine. Benchmarks at >8,000 QPS on Cohere 10M — 2× the previous VectorDBBench #1 (ZillizCloud).

---

## Why in-process matters

Traditional vector DBs (Pinecone, Weaviate, Chroma server mode) require a separate service:

```
Your app → network → vector DB server → network → your app
```

Zvec runs inside your process:

```
Your app → Zvec (in-process) → result
```

No serialisation, no network hop, no server to manage or pay for. The tradeoff: no multi-process sharing (one writer at a time, one process owns the index).

---

## Specs

| Property | Value |
|----------|-------|
| Architecture | In-process C++ library with Python bindings (SWIG) |
| Built on | Proxima — Alibaba's production vector engine |
| Platforms | Linux x86_64, Linux ARM64, macOS ARM64 |
| Install | `pip install zvec` |
| Licence | Apache 2.0 |

---

## Performance

Benchmarked on **VectorDBBench, Cohere 10M dataset**:

| System | QPS |
|--------|-----|
| Zvec | **>8,000** |
| ZillizCloud (previous #1) | ~4,000 |

Also reduces index build time compared to the previous leaderboard leader.

---

## Features

- **Dense + sparse vectors** — FP32 dense, sparse vectors, multi-vector queries
- **Index types** — HNSW, FAISS; DiskANN (v0.5.0+) for disk-backed indexes that cut memory usage on large datasets
- **Hybrid search** — scalar filter + vector similarity in a single query; optional inverted indexes
- **Built-in reranking** — weighted fusion and Reciprocal Rank Fusion (RRF) for multi-vector results
- **Full CRUD + schema evolution** — add/update/delete docs; evolve schema without rebuilding from scratch

---

## Quick start

```python
import zvec

schema = zvec.CollectionSchema(
    name="my_docs",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 1536),
)
collection = zvec.create_and_open(path="./my_index", schema=schema)

# Insert
collection.insert([
    zvec.Doc(id="doc_1", vectors={"embedding": my_embedding_1}),
    zvec.Doc(id="doc_2", vectors={"embedding": my_embedding_2}),
])

# Query
results = collection.query(
    zvec.VectorQuery("embedding", vector=query_embedding),
    topk=10,
)
```

---

## When to use Zvec vs a server DB

| Situation | Use |
|-----------|-----|
| Single-process app, local RAG, edge/mobile | **Zvec** |
| Multi-process access, shared index, team infra | Weaviate / Qdrant / Pinecone |
| Already have turbovec for compression | Both can coexist — zvec indexes, turbovec compresses |

---

## Source & licence

- **GitHub**: [github.com/alibaba/zvec](https://github.com/alibaba/zvec)
- **Docs**: [zvec.org](https://zvec.org)
- **Licence**: Apache 2.0
