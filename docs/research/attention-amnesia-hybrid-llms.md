# Attention Amnesia in Hybrid LLMs

> Source: [arXiv:2606.11052](https://arxiv.org/abs/2606.11052) · June 2026

## TL;DR

Chain-of-thought fine-tuning (CoT-SFT) systematically destroys long-context recall in hybrid linear-attention models. HypeNet-9B drops from **67.2% → 9.4%** on a 256K needle-in-a-haystack task after CoT training. The cause: CoT-SFT biases the query and key projection matrices toward short-range patterns, breaking the routing mechanism for long-range retrieval. The fix — **QK-Restore** — takes 30 minutes with no retraining and recovers most of the lost recall while keeping reasoning gains.

---

## What is attention amnesia?

Hybrid LLMs combine full (softmax) attention layers with linear attention or SSM layers (e.g., Mamba). The full-attention layers are responsible for long-range retrieval; the linear layers handle local sequence modelling cheaply.

When these models are fine-tuned with chain-of-thought data, the training signal concentrates on short reasoning chains. The gradient updates to W_Q and W_K (query/key projections) in the full-attention layers skew toward short-range pattern matching — the model "forgets" how to route attention to distant context.

---

## Affected architectures

Demonstrated on:
- **HypeNet-5B** and **HypeNet-9B**
- **Jet-Nemotron**

These are all hybrid models with a mix of full-attention and linear/SSM layers.

---

## Benchmark: before and after CoT-SFT

| Model | Benchmark | Before CoT-SFT | After CoT-SFT |
|-------|-----------|---------------|---------------|
| HypeNet-9B | NIAH-S2 @ 256K | 67.2% | **9.4%** |
| HypeNet-5B | NIAH-S3 @ 256K | — | 65.4% (pre-fix) |

NIAH = Needle In A Haystack — measures whether the model can retrieve a specific fact embedded in a long document.

---

## Root cause

CoT-SFT biases attention gradients toward **short-range patterns**, corrupting `W_Q` and `W_K` — the matrices that determine which positions attend to which. The long-range routing capability encoded in these projections is overwritten by short-range reasoning training.

The effect is specific to W_Q and W_K. Other parameters (FFN, V projections) are not the cause.

---

## The fix: QK-Restore

A **training-free** post-processing method:

1. After CoT-SFT, revert **only W_Q and W_K** to their pre-SFT values
2. Keep all other fine-tuned parameters (FFN, W_V, layer norms, etc.)
3. Optionally apply **Procrustes alignment** — rotate the restored W_Q/W_K toward the post-SFT values to partially preserve reasoning gains while restoring recall

Result for HypeNet-5B after QK-Restore:
- NIAH-S3 @ 256K: 65.4% → **76.4%** ✓
- Reasoning capability: preserved

Total cost: ~30 minutes, no GPU training.

---

## Why this matters for hybrid model fine-tuning

Anyone fine-tuning hybrid linear-attention models (HypeNet, Zamba, Jamba, Mamba-Transformer variants, Jet-Nemotron) with reasoning data should:

1. Evaluate NIAH performance before and after fine-tuning
2. Apply QK-Restore as a standard post-processing step if recall degrades
3. Prefer Procrustes variant to balance recall recovery with reasoning retention

---

## Source

- **Paper**: [arXiv:2606.11052](https://arxiv.org/abs/2606.11052)
