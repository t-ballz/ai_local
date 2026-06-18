# Hyper-Extract: Typed Knowledge Graph Extraction

> GitHub: [yifanfeng97/Hyper-Extract](https://github.com/yifanfeng97/Hyper-Extract)  
> License: Apache-2.0 · Install: `uv tool install hyperextract`

## TL;DR

Hyper-Extract turns unstructured documents into typed knowledge structures (from simple lists to spatio-temporal graphs) in one command. It decouples the *shape* of the knowledge from the *storage engine*, letting you swap between GraphRAG, LightRAG, KG-Gen, and others without rewriting extraction logic. Supports local deployment via vLLM with open-weight models.

---

## The problem

Most RAG pipelines chunk text and store embeddings — which works for simple question answering but breaks on complex relational or temporal queries. The extraction stage is either skipped (plain chunking) or baked into a specific graph engine (GraphRAG, LightRAG), making it hard to change the backend or reuse the knowledge in a different shape.

Hyper-Extract separates extraction from storage: you describe *what structure you want*, pick an engine, and the tool handles the rest.

---

## Knowledge structure types

| Type | What it captures |
|------|-----------------|
| List / Set | Simple collections |
| Pydantic Model | Typed entity records |
| Knowledge Graph | Entities + relations |
| Hypergraph | N-ary relations (beyond pairs) |
| Temporal Graph | Entities with time-indexed edges |
| Spatial Graph | Entities with spatial coordinates |
| Spatio-Temporal Graph | Both time and space |

---

## Extraction engines

GraphRAG, LightRAG, Hyper-RAG, KG-Gen, Cog-RAG, and 5+ others — selectable per-run without changing extraction code.

---

## Domain templates

80+ zero-code YAML templates across six domains:

- **Finance**: earnings, market events, company relations
- **Legal**: case entities, clauses, parties
- **Medical**: conditions, treatments, outcomes
- **Traditional Chinese Medicine**
- **Industry**: supply chain, manufacturing
- **General**: biography, events, any graph

---

## Usage

```bash
# Install
uv tool install hyperextract

# Configure (OpenAI-compatible API; point at vLLM for local)
he config init -k YOUR_API_KEY

# Extract using a preset template
he parse document.md -t general/biography_graph -o ./output/

# Use a local model via vLLM
he config init --base-url http://localhost:8000/v1 -k dummy
he parse report.pdf -t finance/company_graph -o ./kg/
```

Supported embedding backends for local deployment: `bge-m3` via vLLM, `text-embedding-v4` (Qwen), OpenAI embeddings.

---

## Local deployment

Hyper-Extract uses an OpenAI-compatible API interface, so any vLLM-served model works:

```bash
vllm serve Qwen/Qwen3.5-9B --port 8000
he config init --base-url http://localhost:8000/v1 -k dummy
```

Tested with Qwen3.5-9B; any instruction-following model capable of structured extraction works.

---

## Limitations

- No arXiv paper — GitHub project, no formal benchmarks published
- Extraction quality depends on the base model's instruction-following ability
- Complex hypergraph extraction benefits from a larger model

---

## Source

- **GitHub**: [yifanfeng97/Hyper-Extract](https://github.com/yifanfeng97/Hyper-Extract)
