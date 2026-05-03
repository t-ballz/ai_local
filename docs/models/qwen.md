# Qwen

> Source: [qwenlm.github.io](https://qwenlm.github.io/blog/qwen3/) · [github.com/QwenLM/Qwen3](https://github.com/QwenLM/Qwen3) · [github.com/QwenLM/Qwen3.6](https://github.com/QwenLM/Qwen3.6) · [Qwen3.5 blog](https://qwen.ai/blog?id=qwen3.5)

## TL;DR

Alibaba Cloud's open-weight family. Generations: **Qwen3** (April 2025) → **Qwen3.5** (Feb–Mar 2026) → **Qwen3.6** (2026, confirmed, details TBC). All share hybrid thinking mode, Apache 2.0 licence, and strong coding/math performance. Qwen3.5 adds native vision and 262K context across the range.

---

## Qwen3.5 (Feb–Mar 2026) — current generation

Qwen3.5 adds native **vision** (text + images), **262K context** across all sizes, and maintains hybrid thinking mode. Apache 2.0.

Sizes marked † are confirmed from HuggingFace GGUF repos. Others are estimates (±10–15%).

| Model | Type | Active / Total | Context | GGUF Q4_K_M | Notes |
|-------|------|---------------|---------|------------|-------|
| Qwen3.5-0.8B | Dense | 0.8B | 262K | 0.53 GB† | Vision; edge/mobile |
| Qwen3.5-4B | Dense | 4B | 262K | 2.74 GB† | Vision; strong quality for size |
| Qwen3.5-9B | Dense | 9B | 262K | 5.68 GB† | Vision; top small-model benchmark scores |
| Qwen3.5-27B | Dense | 27B | 262K | ~17 GB | Vision |
| Qwen3.5-35B-A3B | MoE | 3B / 35B | 262K | ~19–22 GB | Vision; successor to Qwen3-30B-A3B |
| Qwen3.5-122B-A10B | MoE | 10B / 122B | 262K | ~70 GB | Vision |
| Qwen3.5-397B-A17B | MoE | 17B / 397B | 262K | ~240 GB | Flagship; multi-node |

---

## Qwen3 (April 2025) — previous generation

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
    Qwen3-30B-A3B runs at 3B active parameters but competes with the dense 32B on many tasks — at roughly the same disk footprint but much faster inference and lower VRAM use. Qwen3.5-35B-A3B is its direct successor.

!!! note "Qwen3.6"
    Qwen3.6 is confirmed to exist (GitHub repo at [github.com/QwenLM/Qwen3.6](https://github.com/QwenLM/Qwen3.6); at minimum a 35B-A3B variant). Full specs not yet documented here — verify before relying on any details.

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
