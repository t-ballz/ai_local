# Llama

> Source: [llama.com](https://www.llama.com) · [github.com/meta-llama/llama-models](https://github.com/meta-llama/llama-models) · [Meta AI blog](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)

## TL;DR

Meta's open-weight model family. Llama 3.x covers dense models from 1B to 405B. Llama 4 (April 2025) switches to MoE and adds native multimodal (text + images). The 3.3 70B dense and 4 Scout MoE are the most popular for local use. Custom Meta Llama License (permissive for most uses; commercial use permitted under 700M MAU threshold).

---

## Llama 3.x — dense models

| Model | Type | Params | Context | GGUF Q4_K_M | RAM (Q4) |
|-------|------|--------|---------|------------|---------|
| Llama 3.2 1B | Dense | 1B | 128K | ~0.7 GB | ~2 GB |
| Llama 3.2 3B | Dense | 3B | 128K | ~2 GB | ~3 GB |
| Llama 3.1 8B | Dense | 8B | 128K | ~4.7 GB | ~6 GB |
| Llama 3.3 70B | Dense | 70B | 128K | ~43 GB | ~48 GB |
| Llama 3.1 405B | Dense | 405B | 128K | ~245 GB | ~270 GB |

**Llama 3.2 1B/3B** — edge/mobile-class; multilingual text. No vision on these sizes.  
**Llama 3.2 11B/90B** — multimodal vision variants; 11B fits on a single 8GB GPU (Q4).  
**Llama 3.3 70B** — best quality/size in the 3.x dense line; matches 3.1 405B quality on many tasks.  
**Llama 3.1 405B** — flagship dense; requires multi-GPU or CPU+RAM offload setup.

---

## Llama 4 — MoE models (April 2025)

| Model | Type | Active / Total | Experts | Context | GGUF Q4_K_M | RAM (Q4) |
|-------|------|---------------|---------|---------|------------|---------|
| Llama 4 Scout | MoE | 17B / 109B | 16 | 10M | ~65 GB | ~65 GB |
| Llama 4 Maverick | MoE | 17B / 400B | 128 | 1M | ~243 GB | ~250 GB |

!!! note "MoE RAM cost"
    All parameters must be loaded even though only 17B activate per token. Scout at Q4_K_M needs ~65 GB total — a 24 GB GPU can run it at shorter context lengths.

!!! tip "Llama 4 Scout sweet spots"
    Single RTX 4090 (24 GB) handles Q4 at 8K–16K context. Mac M3 Max (128 GB unified) runs Q8 comfortably.

---

## Strengths & use cases

| Model | Best for |
|-------|---------|
| 3.2 1B / 3B | On-device / embedded, fast inference, simple tasks |
| 3.1 8B / 3.3 70B | General assistant, coding, RAG |
| 4 Scout | Very long documents (10M ctx), multimodal, single-GPU MoE |
| 4 Maverick | High-quality multimodal, coding, complex reasoning, multi-GPU setups |

Llama 4 Maverick benchmarks: 73.4 MMMU (image reasoning), 43.4 LiveCodeBench, 80.5 MMLU Pro — competitive with GPT-4o and DeepSeek V3 at half the active parameters.

---

## Source & licence

- **Source**: [github.com/meta-llama/llama-models](https://github.com/meta-llama/llama-models)
- **Licence**: Meta Llama License (open weights; commercial use allowed under 700M MAU)
- **GGUF models**: search `meta-llama` or `bartowski` on [huggingface.co](https://huggingface.co)
