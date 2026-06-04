# Gemma

> Source: [ai.google.dev/gemma](https://ai.google.dev/gemma/docs/core) · [github.com/google-deepmind/gemma](https://github.com/google-deepmind/gemma) · [Gemma 4 blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) · [HuggingFace Gemma 4](https://huggingface.co/blog/gemma4)

## TL;DR

Google DeepMind's open-weight family. Gemma 3 (March 2025) brought 128K context and multimodal (text + images) to small models. Gemma 4 (April–June 2026) adds MoE, video understanding, and a massive coding improvement. A new **12B dense** variant (June 3, 2026) fills the gap between the edge models and the 26B MoE with full audio+video+image support and 256K context at ~6.5 GB Q4. Apache 2.0 licence.

---

## Gemma 3 (March 2025) — dense, multimodal

| Model | Type | Params | Context | GGUF Q4_K_M | RAM (Q4) |
|-------|------|--------|---------|------------|---------|
| Gemma 3 1B | Dense | 1B | 32K | ~0.8 GB | ~1.5 GB |
| Gemma 3 4B | Dense | 4B | 128K | ~2.5 GB | ~4 GB |
| Gemma 3 12B | Dense | 12B | 128K | ~7.5 GB | ~9 GB |
| Gemma 3 27B | Dense | 27B | 32K | ~17 GB | ~20 GB |

All Gemma 3 models support **text + images** (multimodal). 140+ languages. Context is 128K for 1B–12B; 27B uses 32K.

---

## Gemma 4 (April–June 2026) — current generation

| Model | Type | Params | Context | GGUF Q4 approx | Released |
|-------|------|--------|---------|---------------|---------|
| Gemma 4 E2B | Dense (PLE) | ~2B eff. | 128K | ~1.5 GB | Apr 2026 |
| Gemma 4 E4B | Dense (PLE) | ~4B eff. | 128K | ~2.7 GB | Apr 2026 |
| **Gemma 4 12B** | Dense | 11.95B | 256K | **~6.5 GB est.** | Jun 3 2026 |
| Gemma 4 26B-A4B | MoE | 3.8B / 26B | 256K | ~16 GB | Apr 2026 |
| Gemma 4 31B | Dense | 31B | 256K | ~20 GB | Apr 2026 |

!!! note "E2B / E4B vs 12B architecture"
    E2B/E4B use **Per-Layer Embeddings (PLE)** — a parameter-efficient edge design, 128K context. The 12B uses a standard dense decoder with **encoder-free** unified multimodal projection (no separate vision/audio encoder), giving it 256K context and stronger per-token quality.

!!! tip "12B sweet spot"
    At ~6.5 GB Q4, Gemma 4 12B fits on an 8 GB GPU (RTX 3070, etc.) while offering full audio + video + image + text and 256K context — a better-rounded option than the 26B-A4B if VRAM is limited.

!!! tip "MoE speed advantage"
    Gemma 4 26B-A4B activates only 3.8B parameters per token — very fast inference at ~16 GB disk size.

All Gemma 4 models support **text + images + video**. E2B, E4B, and **12B** additionally accept **audio input** (ASR + speech translation; 12B uses encoder-free design, max ~30 s clips).

**Gemma 4 benchmarks:**

| Model | MMLU-Pro | LiveCodeBench | GPQA Diamond | Arena rank |
|-------|----------|--------------|-------------|------------|
| 31B | 85.2% | 80.0% | — | #3 open model |
| 26B-A4B | 82.6% | — | — | #6 open model |
| **12B** | **77.2%** | **72.0%** | **78.8%** | — |

---

## Strengths & use cases

| Use case | Recommended |
|----------|------------|
| On-device / mobile | Gemma 4 E2B, E4B |
| Light local inference | Gemma 3 4B, Gemma 4 E4B |
| Vision + audio + OCR (8 GB GPU) | Gemma 4 12B |
| Vision + OCR + document parsing | Gemma 3 12B / 27B, Gemma 4 31B |
| Coding (local, single GPU) | Gemma 4 31B, Gemma 4 12B |
| Agentic workflows / tool use | Gemma 4 26B-A4B or 31B |
| Fine-tuning base | Gemma 3 4B / 12B (well-supported) |

**Gemma 4 31B coding jump**: LiveCodeBench improved from 29.1% (Gemma 3 27B) → **80.0%** — a step-change improvement that makes it a strong local coding assistant on a 24 GB GPU.

**Multimodal strengths (all Gemma 3+)**:
- OCR including handwriting and multilingual text
- Chart and graph comprehension
- Document / PDF parsing
- Screen and UI understanding
- Video understanding (Gemma 4)

---

## Source & licence

- **Source**: [github.com/google-deepmind/gemma](https://github.com/google-deepmind/gemma)
- **Licence**: Apache 2.0 (Gemma 3 and Gemma 4)
- **GGUF models**: search `google/gemma` on [huggingface.co](https://huggingface.co) or `ollama pull gemma3` / `ollama pull gemma4`
