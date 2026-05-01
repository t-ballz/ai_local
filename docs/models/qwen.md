# Qwen

> Source: [qwenlm.github.io](https://qwenlm.github.io/blog/qwen3/) · [github.com/QwenLM/Qwen3](https://github.com/QwenLM/Qwen3) · [Qwen3 technical report](https://arxiv.org/abs/2505.09388)

## TL;DR

Alibaba Cloud's open-weight family. Qwen3 (April 2025) is the current generation: six dense sizes (0.6B–32B) plus two efficient MoE models (30B-A3B and 235B-A22B). Key differentiator: built-in **hybrid thinking mode** — a single model can reason step-by-step or reply instantly, toggled via a system prompt flag. Apache 2.0 licence.

---

## Qwen3 — model variants

| Model | Type | Active / Total | Context | Ollama size | RAM (Q4) |
|-------|------|---------------|---------|------------|---------|
| Qwen3-0.6B | Dense | 0.6B | 40K | 0.5 GB | ~1 GB |
| Qwen3-1.7B | Dense | 1.7B | 40K | 1.4 GB | ~2 GB |
| Qwen3-4B | Dense | 4B | 256K | 2.5 GB | ~4 GB |
| Qwen3-8B | Dense | 8B | 40K | 5.2 GB | ~7 GB |
| Qwen3-14B | Dense | 14B | 40K | 9.3 GB | ~10 GB |
| Qwen3-30B-A3B | MoE | 3B / 30B | 256K | 19 GB | ~20 GB |
| Qwen3-32B | Dense | 32B | 40K | 20 GB | ~22 GB |
| Qwen3-235B-A22B | MoE | 22B / 235B | 256K | 142 GB | ~145 GB |

!!! tip "MoE efficiency"
    Qwen3-30B-A3B runs at 3B active parameters but competes with the dense 32B on many tasks — at roughly the same disk footprint but much faster inference and lower VRAM use.

!!! note "Context window"
    The native context of most models is 40K tokens, but the architecture supports extension to 256K–1M with RoPE scaling. The 4B and 30B-A3B are natively trained at 256K.

---

## Hybrid thinking mode

Qwen3 supports two modes in a single model:

| Mode | Trigger | When to use |
|------|---------|-------------|
| Thinking | `/think` in system prompt | Math, coding, complex reasoning |
| Non-thinking | `/no_think` (default) | Conversational, fast replies |

Thinking mode activates an internal chain-of-thought (like DeepSeek R1) before producing the final answer.

---

## Strengths & use cases

| Use case | Recommended |
|----------|------------|
| Edge / embedded | Qwen3-0.6B, 1.7B |
| Budget GPU (8 GB VRAM) | Qwen3-4B, 8B |
| Coding & math (mid tier) | Qwen3-14B, 30B-A3B |
| High-quality local reasoning | Qwen3-32B |
| Flagship (multi-GPU) | Qwen3-235B-A22B |

- **Coding & math**: among the strongest open-weight models at each size tier
- **Multilingual**: 119 languages, trained on ~36T tokens
- **Agentic / tool use**: supports function calling and structured output in both thinking and non-thinking modes
- Qwen3-4B reportedly rivals Qwen2.5-72B on many benchmarks

---

## Source & licence

- **Source**: [github.com/QwenLM/Qwen3](https://github.com/QwenLM/Qwen3)
- **Licence**: Apache 2.0
- **GGUF models**: search `Qwen` on [huggingface.co](https://huggingface.co) or `ollama pull qwen3`
