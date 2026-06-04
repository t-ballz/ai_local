# Holo

> Source: [hcompany.ai](https://hcompany.ai/holo3.1) · [HuggingFace Hcompany](https://huggingface.co/Hcompany) · [HuggingFace blog](https://huggingface.co/blog/Hcompany/holo31)

## TL;DR

H Company's (French) open-weight Vision-Language Model family built for **computer-use agents** — screen understanding, GUI navigation, and automation. Holo 3.1 (June 2, 2026) is based on the Qwen 3.5 architecture and comes in four sizes from 0.8B to 35B-A3B. Runs on a 12 GB GPU at 140 ms latency. Apache 2.0.

---

## Holo 3.1 (June 2026) — current generation

| Model | Type | Active / Total | Context | GGUF Q4 | Notes |
|-------|------|---------------|---------|---------|-------|
| Holo-3.1-0.8B | Dense | 0.8B | 64K | ~0.5 GB | Edge/mobile |
| Holo-3.1-4B | Dense | 4B | 64K | ~2.5 GB | |
| Holo-3.1-9B | Dense | 9B | 64K | ~5.5 GB | |
| Holo-3.1-35B-A3B | MoE | 3B / 35B | 64K | ~20 GB | Flagship; best benchmark scores |

Based on Qwen 3.5 family. Architecture separates a **Vision Encoder** from an **Action Controller**, both tuned for UI grounding tasks. Quantizations: BF16, FP8, NVFP4, Q4 GGUF (FP8/NVFP4 degrade OSWorld scores by only ~2 points vs BF16).

---

## Benchmarks (Holo 3.1)

| Benchmark | Score | vs. Holo 3.0 |
|-----------|-------|-------------|
| OSWorld (desktop automation) | 74.2% | +6.1 pp |
| AndroidWorld 35B-A3B | 79.3% | +12.3 pp |
| AndroidWorld 4B / 9B | 71% | +13 pp |

OSWorld 74.2% is state-of-the-art among openly available computer-use models.

---

## What it does

Holo is purpose-built for **agentic computer use**, not general conversation. It takes screenshots (or screen recordings) as input and outputs actions — clicks, keystrokes, form fills, navigation steps.

| Use case | Notes |
|----------|-------|
| Browser automation | Navigate web apps, fill forms, extract data |
| Desktop app control | File management, GUI workflows |
| Mobile automation | Android UI navigation (AndroidWorld benchmark) |
| Enterprise workflows | CRM data entry, ERP navigation, financial auditing |

It is **not** a general-purpose assistant — do not evaluate it on MMLU or coding benchmarks.

---

## Running locally

```bash
# Ollama (if Holo is added to registry)
# ollama pull holo3.1

# Direct via llama.cpp / LM Studio
# Download GGUF from huggingface.co/Hcompany
```

The 9B model fits in 8 GB VRAM (Q4). The 35B-A3B flagship needs ~20 GB for the weights — fits on a 24 GB GPU at reasonable context.

Pairs well with a screen-capture tool and an action-execution framework (e.g. `computer_use` Python library, Playwright for browser tasks).

---

## Source & licence

- **Source**: [huggingface.co/Hcompany](https://huggingface.co/Hcompany)
- **Licence**: Apache 2.0
- **GGUF models**: search `Hcompany/Holo-3.1` on [huggingface.co](https://huggingface.co)
