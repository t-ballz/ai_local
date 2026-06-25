# Grouped Query Experts: Applying MoE Routing to Self-Attention

> Source: [arXiv:2606.20945](https://arxiv.org/abs/2606.20945) · Jun 2026  
> Authors: Vishesh Tripathi, Abhay Kumar

## TL;DR

Grouped Query Experts (GQE) applies Mixture-of-Experts routing to GQA self-attention: a router activates ~50% of query-head experts per token while keeping key-value heads fully dense. On a 250M parameter model trained for 30B tokens, GQE matches the all-active GQA baseline in downstream accuracy while cutting active query-head compute by half, with 1.67–1.80× speedups at long context lengths.

---

## The problem

At long context lengths, self-attention is the dominant compute cost in transformer inference. GQA (Grouped Query Attention) already reduces KV cache size, but the query-head computation still scales with sequence length. MoE routing has shown dramatic compute savings in feedforward layers — but applying it to attention is non-trivial because attention requires all keys and values to be globally consistent.

---

## How it works

GQE keeps KV heads fully dense and unchanged — critical for maintaining the global attention pattern. Only query heads are sparsified via MoE routing:

- A lightweight router assigns each token to ~50% of query-head experts
- Each expert is a group of query heads
- Token-expert routing uses standard top-k selection
- KV cache benefits of GQA are fully preserved since KV heads are untouched

This design avoids the key challenge of applying MoE to attention (inconsistent KV state) by restricting sparsity to queries only.

The model is trained end-to-end with routing and attention jointly — no separate training stages.

---

## Results

On 250M parameter scale, 30B token training budget:

| Setup | Downstream accuracy | Active query-head compute |
|---|---|---|
| GQA (all-active baseline) | Baseline | 100% |
| GQE (50% query experts) | Matches baseline | ~50% |

Long-context speedups:
- **1.67×** at moderate context lengths
- **1.80×** at longer context lengths

The speedup grows with context length — exactly where attention cost is highest.

---

## Why it matters for local AI

This is a practically applicable technique for making large models faster at long contexts:

- **Drop-in architectural change**: Works with GQA — already standard in most modern open-weight models (Llama, Qwen, Mistral, Gemma)
- **KV cache unchanged**: No cache format changes; compatible with existing KV caching implementations
- **No accuracy loss**: Half the query compute with no measurable quality drop at 250M scale
- **Long-context workloads**: The gains compound at 8K+ context lengths, where attention already dominates compute

The main unknown is scaling behavior — 250M is small, and whether the accuracy parity holds at 7B+ remains to be validated.

---

## Limitations

- Evaluated at 250M parameter scale only; larger model validation is needed
- Router overhead adds some latency — net speedup depends on routing implementation efficiency
- Interaction with speculative decoding, flash attention variants, and sliding window attention not studied

---

## Source

- **Paper**: [arXiv:2606.20945](https://arxiv.org/abs/2606.20945)
- **Preprint date**: Jun 2026
