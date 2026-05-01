# DeepSeek

> Source: [github.com/deepseek-ai](https://github.com/deepseek-ai) · [DeepSeek-R1 paper (HF)](https://huggingface.co/deepseek-ai/DeepSeek-R1) · [V3 technical report](https://arxiv.org/html/2412.19437v1)

## TL;DR

Chinese AI lab DeepSeek's open-weight models, famous for cost-efficient training. Two lines: **V-series** (general purpose, MoE) and **R-series** (reasoning, chain-of-thought). The R1 distills bring frontier reasoning to consumer hardware. MIT licence on distills; DeepSeek licence on the full 671B models.

---

## Model lines

### V-series — general purpose (MoE)

| Model | Type | Active / Total | Context | GGUF Q4_K_M | RAM (Q4) |
|-------|------|---------------|---------|------------|---------|
| DeepSeek-V3 | MoE | 37B / 671B | 128K | ~404 GB | ~420 GB |
| DeepSeek-V3-0324 | MoE | 37B / 671B | 128K | ~404 GB | ~420 GB |
| DeepSeek-V3.1 | MoE | 37B / 671B | 128K | ~404 GB | ~420 GB |
| DeepSeek-V4 | MoE | ~37B / ~671B | 1M | TBD | TBD |

V3.1 (August 2025) adds hybrid thinking/non-thinking mode identical to Qwen3's approach — switching via chat template, no separate model needed.

### R-series — reasoning (MoE)

| Model | Type | Active / Total | Context | Notes |
|-------|------|---------------|---------|-------|
| DeepSeek-R1 | MoE | 37B / 671B | 128K | Pure chain-of-thought reasoning |
| DeepSeek-R1-0528 | MoE | 37B / 671B | 128K | Updated, stronger reasoning |

The full R1 requires ~404 GB at Q4_K_M — multi-node territory.

### R1 Distills — dense, consumer-friendly

DeepSeek distilled R1's reasoning into smaller dense models (Qwen2.5 and Llama 3 bases), making chain-of-thought reasoning accessible on a single GPU:

| Model | Base | GGUF Q4_K_M | RAM (Q4) | VRAM needed |
|-------|------|------------|---------|------------|
| R1-Distill-Qwen-1.5B | Qwen2.5-1.5B | ~1 GB | ~1.5 GB | 2 GB |
| R1-Distill-Qwen-7B | Qwen2.5-7B | ~4.5 GB | ~6 GB | 6 GB |
| R1-Distill-Llama-8B | Llama3.1-8B | ~5 GB | ~6 GB | 8 GB |
| R1-Distill-Qwen-14B | Qwen2.5-14B | ~9 GB | ~10 GB | 10 GB |
| R1-Distill-Qwen-32B | Qwen2.5-32B | ~19 GB | ~22 GB | 24 GB |
| R1-Distill-Llama-70B | Llama3.3-70B | ~43 GB | ~48 GB | 48 GB+ |

---

## Strengths & use cases

| Model | Best for |
|-------|---------|
| R1-Distill-Qwen-7B / 8B | Reasoning on 8 GB VRAM; strong math |
| R1-Distill-Qwen-14B | Best quality in the 10 GB VRAM range |
| R1-Distill-Qwen-32B | Outperforms OpenAI o1-mini; single 24 GB GPU |
| R1-Distill-Llama-70B | Near-full R1 quality; 94.5% MATH-500, 57.5 LiveCodeBench |
| V3 / V3.1 (cloud/multi-GPU) | Fast general-purpose chat; hybrid reasoning + general |

**R1 distills are particularly strong at:**
- Mathematical proofs and STEM problem solving
- Code generation and debugging
- Structured logical reasoning
- Tasks benefiting from visible thinking (the `<think>` trace is inspectable)

!!! tip "Best local pick"
    `R1-Distill-Qwen-32B` at Q4_K_M on a 24 GB GPU (e.g., RTX 4090) is the community sweet spot: frontier-class reasoning without multi-GPU requirements.

---

## Source & licence

- **R1 / distills**: [github.com/deepseek-ai/DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1) — MIT licence
- **V3**: [github.com/deepseek-ai/DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3) — DeepSeek Model Licence
- **GGUF models**: search `bartowski/DeepSeek` or `unsloth/DeepSeek` on [huggingface.co](https://huggingface.co)
