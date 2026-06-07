# TurboQuant — KV Cache Compression

> Source: [ICLR 2026 paper (Zandieh et al.)](https://arxiv.org/abs) · [llama.cpp discussion #20969](https://github.com/ggml-org/llama.cpp/discussions/20969) · [0xSero/turboquant](https://github.com/0xSero/turboquant) · [SaschaOnTour/turboquant](https://github.com/SaschaOnTour/turboquant)

## TL;DR

A training-free, data-oblivious algorithm that compresses the LLM **KV cache** to 3 bits per value. Published by Google Research at ICLR 2026. Result: **6× memory reduction** with negligible accuracy loss and **up to 8× attention speedup** on H100 — no retraining or calibration data required. Also powers the [turbovec](../tools/turbovec.md) vector index.

---

## Why KV cache compression matters

At long context lengths, the KV cache dominates GPU memory — for a 70B model at 128K context the FP16 KV cache alone can consume tens of gigabytes, limiting batch size and usable context length. TurboQuant shrinks this at inference time without touching the model weights.

---

## How it works

Two-stage pipeline applied to each key and value tensor as it enters the cache:

1. **PolarQuant** — applies a random orthogonal rotation to each K/V vector before quantization. This distributes energy evenly across all dimensions so no single coordinate dominates, enabling efficient low-bit representation.
2. **QJL (Quantized Johnson-Lindenstrauss)** — a 1-bit error-correction step using a random matrix derived from the JL lemma. Reduces residual approximation error in the attention dot-product computation.

The combined effect: 3-bit KV quantization with ~6× size reduction. No calibration data, no retraining.

---

## Performance

| Metric | Value |
|--------|-------|
| KV cache compression | ~6× (FP16 → 3 bit) |
| Attention computation speedup | Up to 8× (H100) |
| Quality degradation | Negligible |
| Training required | None |
| Calibration data | None |

With the 0xSero community implementation (3-bit keys, 2-bit values) at 32K context, total VRAM drops to ~49% of FP16 baseline — effectively doubling usable batch size on a fixed GPU.

---

## Community implementations

| Project | Backend | Notes |
|---------|---------|-------|
| [0xSero/turboquant](https://github.com/0xSero/turboquant) | Triton + vLLM | 3-bit keys, 2-bit values; ~20% of FP16 KV cache, ~49% total VRAM at 32K |
| [SaschaOnTour/turboquant](https://github.com/SaschaOnTour/turboquant) | Rust + CUDA + mistral.rs | Drops QJL, adds PQO variant with fused CUDA kernel |
| llama.cpp | tracking | Discussion #20969 — upstream integration in progress |

---

## Relationship to turbovec

The same TurboQuant algorithm is used by [turbovec](../tools/turbovec.md) to compress static embedding vectors for local RAG — same math, different target (stored embeddings vs. live KV cache).
