# Mellum

> Source: [jetbrains.com/mellum](https://www.jetbrains.com/mellum/) · [HuggingFace JetBrains](https://huggingface.co/JetBrains) · [technical report](https://arxiv.org/abs/2605.31268)

## TL;DR

JetBrains' open-weight coding model family. Mellum 2 (June 1, 2026) is a 12B-total / 2.5B-active sparse MoE model trained for code generation, agentic workflows, and lightweight orchestration in multi-model systems. Claims 2× faster inference vs comparable-sized dense models. Apache 2.0.

---

## Mellum 2 (June 2026) — current generation

| Model | Type | Active / Total | Context | GGUF Q4_K_M | Notes |
|-------|------|---------------|---------|------------|-------|
| Mellum2-12B-A2.5B-Base | MoE | 2.5B / 12B | 128K | ~6–7 GB | Base weights |
| Mellum2-12B-A2.5B-Instruct | MoE | 2.5B / 12B | 128K | ~6–7 GB | Instruction-tuned |

64 total experts, 8 active per token. 1024-token sliding window attention. Architecture support merged into llama.cpp at release b9482.

!!! note "GGUF quantization quirk"
    Some expert tensors have width 896, which is not divisible by standard GGUF block sizes. Certain quantizers fall back to Q5_0 or Q8_0 for those tensors. If you see degraded Q4_K_M quality, try a Q6_K or Q8_0 build, or use a GGUF from a provider that handles this (e.g. bartowski).

---

## Benchmarks (Mellum2-12B-A2.5B)

| Benchmark | Score |
|-----------|-------|
| HumanEval | 41.5% |
| MBPP | 62.4% |
| GSM8K | 81.7% |
| MMLU | 70.9% |
| BBH | 74.9% |

Claims 2× faster inference than comparable-size dense models due to sparse activation (only 2.5B params active per token despite 12B total).

---

## Generation history

| Version | Params | Focus |
|---------|--------|-------|
| Mellum 1 | 4B dense | Code completion inside JetBrains IDEs only |
| **Mellum 2** | 12B MoE (2.5B active) | Code gen, agentic tasks, multi-model orchestration |

Mellum 2 is significantly broader than Mellum 1: it supports tool calling, multi-step reasoning, natural language understanding, and works as a sub-agent or router in larger pipelines — not just inline autocomplete.

---

## Strengths & use cases

| Use case | Notes |
|----------|-------|
| Code generation / editing | Primary use; HumanEval, MBPP trained |
| Sub-agent in multi-model pipeline | Low latency; good at routing and classification |
| Context compression / summarisation | Handles long conversations (128K ctx) |
| Tool selection / prompt classification | Efficient at 2.5B active params |
| Private/on-prem deployment | Open weights, no telemetry requirement |

The sparse activation makes it an efficient **specialist component** — run it alongside a larger general model, with Mellum handling latency-sensitive steps.

---

## Running locally

```bash
# Ollama
ollama pull mellum2

# llama.cpp (needs build b9482+)
# Download from huggingface.co/JetBrains/Mellum2-12B-A2.5B-Instruct-GGUF
```

At ~6–7 GB Q4_K_M, Mellum 2 fits on any 8 GB GPU.

---

## Source & licence

- **Source**: [github.com/JetBrains-Research/Mellum](https://github.com/JetBrains-Research/Mellum)
- **Licence**: Apache 2.0
- **GGUF models**: [huggingface.co/JetBrains](https://huggingface.co/JetBrains)
