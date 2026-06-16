# MiniMax Sparse Attention

> Source: [arXiv:2606.13392](https://arxiv.org/abs/2606.13392) · MiniMax · June 2026  
> HuggingFace: [papers/2606.13392](https://huggingface.co/papers/2606.13392)

## TL;DR

Softmax attention scales quadratically with context length — at 1M tokens, this is completely intractable. MiniMax Sparse Attention (MSA) solves it with a two-branch architecture: a lightweight **index branch** predicts which KV blocks matter per attention group, and a **main branch** does exact attention only on those blocks. Result: **28.4× fewer attention operations** and **14.2× prefill speedup** at 1M context on H800 GPUs, with no quality loss. Ships as the production attention mechanism in MiniMax-M3 (109B).

---

## The problem

Full softmax attention at 1M context length is quadratically expensive — untenable at deployment scale even on high-end hardware. Sparse attention is the general answer, but the challenge is *which tokens to attend to*: random or fixed patterns miss important context; learning patterns adds overhead.

---

## How MSA works

Two branches run in parallel:

### Index branch

A lightweight scorer that — independently per GQA group — selects the top-k KV **blocks** most relevant to the current query. The selection is group-specific: different attention heads can select different blocks based on what each head tends to look for.

### Main branch

Performs exact block-sparse attention only on the blocks selected by the index branch. No approximation within the selected blocks — full attention quality, just over a sparse subset.

The unit of sparsity is a **block** of tokens (not individual tokens), which maps efficiently to GPU memory access patterns.

---

## Benchmarks

Measured on MiniMax-M3 (109B, native multimodal) at 1M context on H800 GPUs:

| Metric | Result |
|--------|--------|
| Attention compute reduction | **28.4×** |
| Prefill wall-clock speedup | **14.2×** |
| Decoding wall-clock speedup | **7.6×** |
| Quality vs full GQA | Parity |

---

## Relation to MiniMax-M3

MSA is not just a research contribution — it is the production attention mechanism deployed in **MiniMax-M3**, MiniMax's publicly released 109B multimodal model. The paper describes the technique that makes M3's long-context performance practical at serving scale.

---

## Source

- **Paper**: [arXiv:2606.13392](https://arxiv.org/abs/2606.13392)
