# Qwen3 Embedding & Reranker

> Source: [Qwen blog](https://qwenlm.github.io/blog/qwen3-embedding/) · Alibaba / Qwen team · June 2026  
> Paper: [arXiv:2506.05176](https://arxiv.org/abs/2506.05176)  
> HuggingFace: [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) · [4B](https://huggingface.co/Qwen/Qwen3-Embedding-4B) · [8B](https://huggingface.co/Qwen/Qwen3-Embedding-8B)

## TL;DR

Six open-weight models (three embedding, three reranking) built on Qwen3's foundation. The 8B embedding model holds **#1 on the MTEB multilingual leaderboard** (score 70.58). All sizes run locally via Ollama. Supports 100+ languages including code, 32K–40K context, and instruction-aware prompting for task-specific tuning.

---

## Model lineup

### Embedding models

| Model | Params | Embedding dim | Context | Ollama size |
|-------|--------|--------------|---------|-------------|
| Qwen3-Embedding-0.6B | 0.6B | 1024 (32–1024) | 32K | 639 MB |
| Qwen3-Embedding-4B | 4B | 2560 (custom) | 40K | 2.5 GB |
| Qwen3-Embedding-8B | 8B | 4096 (custom) | 40K | 4.7 GB |

All support **Matryoshka Representation Learning (MRL)** — you can truncate embeddings to smaller dimensions without retraining.

### Reranker models

| Model | Params | MTEB-R | CMTEB-R | MMTEB-R | MLDR |
|-------|--------|--------|---------|---------|------|
| Qwen3-Reranker-0.6B | 0.6B | — | — | — | — |
| Qwen3-Reranker-4B | 4B | **69.76** | 75.94 | 72.74 | 69.97 |
| Qwen3-Reranker-8B | 8B | 69.02 | **77.45** | **72.94** | **70.19** |

---

## Architecture & training

Built on the Qwen3 generative model backbone (decoder-only, repurposed as an encoder via last-token pooling for embeddings). Three-stage training:

1. **Contrastive pre-training** on large weakly-supervised text pairs
2. **Supervised fine-tuning** on high-quality labelled data
3. **Model merging** across checkpoints for stability

An **instruction-aware prompt system** uses Qwen3's generation capability to synthesise task- and language-specific training pairs on the fly — so the model understands prompts like `"Retrieve a passage that answers this question"` and adjusts its representation accordingly.

---

## Capabilities

- **Tasks**: text retrieval, code retrieval, semantic similarity, classification, clustering, bitext mining
- **Languages**: 100+ natural languages + major programming languages
- **Context**: 32K tokens (0.6B), 40K tokens (4B/8B)
- **Instruction-following**: pass a task-specific instruction prefix to shift the embedding space

---

## Local usage

### Ollama

```bash
ollama pull qwen3-embedding          # pulls 8B by default (4.7 GB)
ollama pull qwen3-embedding:0.6b     # 639 MB, fits anywhere

curl http://localhost:11434/api/embed \
  -d '{"model": "qwen3-embedding:0.6b", "input": "Why is the sky blue?"}'
```

### sentence-transformers

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
embeddings = model.encode(["Hello world", "Bonjour le monde"])
```

### transformers (manual pooling)

```python
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
model = AutoModel.from_pretrained("Qwen/Qwen3-Embedding-0.6B")
# last-token pooling on the decoder output
```

### With instruction prefix

```python
instruction = "Retrieve a passage that answers this question: "
query_embedding = model.encode(instruction + "What is the capital of France?")
```

---

## Benchmarks

The 8B model is **#1 on the MTEB multilingual leaderboard** with a score of **70.58** (June 2026). All three sizes rank competitively across English (BEIR/MTEB), multilingual (MIRACL, MMTEB), and code retrieval benchmarks.

---

## License

Apache 2.0. Available on HuggingFace and ModelScope.
