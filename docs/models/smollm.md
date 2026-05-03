# SmolLM3

> Source: [huggingface.co/HuggingFaceTB/SmolLM3-3B](https://huggingface.co/HuggingFaceTB/SmolLM3-3B) · [tinyweights.dev SmolLM3 overview](https://tinyweights.dev/posts/smollm3-3b-the-fully-ope/)

## TL;DR

HuggingFace's open small language model. SmolLM3 (2025) is a 3B-parameter model trained on 11.2 trillion tokens, with 128K context, dual-mode reasoning (think/non-think), and multilingual support — matching or beating several 4B-class models. Apache 2.0. Currently a single size (3B only).

---

## SmolLM3 — model variants

GGUF sizes confirmed from [bartowski/HuggingFaceTB_SmolLM3-3B-GGUF](https://huggingface.co/bartowski/HuggingFaceTB_SmolLM3-3B-GGUF).

| Model | Type | Params | Context | GGUF Q4_K_M | GGUF Q8_0 |
|-------|------|--------|---------|------------|----------|
| SmolLM3-3B | Dense | 3B | 128K | 1.92 GB | 3.28 GB |

---

## Hybrid thinking mode

Like Qwen3, SmolLM3 ships a single model that supports both modes:

| Mode | When to use |
|------|------------|
| Thinking (`/think`) | Reasoning tasks, math, step-by-step problems |
| Non-thinking (default) | Fast conversational replies |

---

## Strengths & use cases

| Use case | Notes |
|----------|-------|
| Tight VRAM budgets (4 GB) | 1.92 GB leaves plenty of headroom for KV cache |
| Edge / embedded | Small enough for CPU-only inference |
| Reasoning on constrained hardware | Dual-mode thinking without needing a separate model |
| Multilingual | Trained for multilingual capability |

At 3B parameters and 1.92 GB Q4_K_M, SmolLM3 fits comfortably on the oldest hardware in this wiki (GTX 1050 Ti with 4 GB VRAM) while offering 128K context and reasoning mode — a notable step up from same-size alternatives.

---

## Source & licence

- **Source**: [github.com/huggingface/smollm](https://github.com/huggingface/smollm)
- **Licence**: Apache 2.0
- **GGUF models**: [bartowski/HuggingFaceTB_SmolLM3-3B-GGUF](https://huggingface.co/bartowski/HuggingFaceTB_SmolLM3-3B-GGUF) · [ggml-org/SmolLM3-3B-GGUF](https://huggingface.co/ggml-org/SmolLM3-3B-GGUF)
- **Ollama**: `ollama pull smollm3`
