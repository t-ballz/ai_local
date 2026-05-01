# Gemma

> Source: [ai.google.dev/gemma](https://ai.google.dev/gemma/docs/core) · [github.com/google-deepmind/gemma](https://github.com/google-deepmind/gemma) · [Gemma 4 blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/) · [HuggingFace Gemma 4](https://huggingface.co/blog/gemma4)

## TL;DR

Google DeepMind's open-weight family. Gemma 3 (March 2025) brought 128K context and multimodal (text + images) to small models. Gemma 4 (April 2026) adds MoE, video understanding, and a massive coding improvement — the 31B hits 80% on LiveCodeBench. Apache 2.0 licence.

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

## Gemma 4 (April 2026) — MoE + multimodal + video

| Model | Type | Active / Total | Context | GGUF Q4 approx | RAM (Q4) |
|-------|------|---------------|---------|---------------|---------|
| Gemma 4 E2B | Dense | ~2B eff. | 128K | ~1.5 GB | ~5 GB |
| Gemma 4 E4B | Dense | ~4B eff. | 128K | ~2.7 GB | ~8 GB |
| Gemma 4 26B-A4B | MoE | 3.8B / 26B | 256K | ~16 GB | ~18 GB |
| Gemma 4 31B | Dense | 31B | 256K | ~20 GB | ~22 GB |

!!! note "E2B / E4B naming"
    "Effective 2B/4B" — these are Gemma 4's edge models, optimised for mobile and low-power hardware while matching much larger Gemma 3 models in quality.

!!! tip "MoE speed advantage"
    Gemma 4 26B-A4B activates only 3.8B parameters per token — very fast inference at ~16 GB disk size.

All Gemma 4 models support **text + images + video** and natively handle structured output, function calling, and tool use.

---

## Strengths & use cases

| Use case | Recommended |
|----------|------------|
| On-device / mobile | Gemma 4 E2B, E4B |
| Light local inference | Gemma 3 4B, Gemma 4 E4B |
| Vision + OCR + document parsing | Gemma 3 12B / 27B, Gemma 4 31B |
| Coding (local, single GPU) | Gemma 4 31B |
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
