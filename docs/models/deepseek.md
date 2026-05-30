# DeepSeek

> Source: [github.com/deepseek-ai](https://github.com/deepseek-ai) · [DeepSeek-R1 paper (HF)](https://huggingface.co/deepseek-ai/DeepSeek-R1) · [V3 technical report](https://arxiv.org/html/2412.19437v1)

## TL;DR

Chinese AI lab DeepSeek's open-weight models, famous for cost-efficient training. Current generation: **V4** (April 2026, MIT) with optional thinking mode, 1M context, and a new CSA+HCA attention architecture. The R1 distills remain the best local reasoning option — small dense models with full chain-of-thought capability. All current flagship and distill models: MIT licence.

---

## V-series — general purpose (MoE)

### DeepSeek V4 (April 2026) — current generation

| Model | Type | Active / Total | Context | Notes |
|-------|------|---------------|---------|-------|
| DeepSeek-V4-Pro | MoE | 49B / 1,600B | 1M | Flagship; multi-node only |
| DeepSeek-V4-Flash | MoE | 13B / 284B | 1M | Faster/smaller V4 variant |

V4 introduces a new **CSA + HCA attention** design that reduces FLOPs to 27% and KV cache to 10% of V3. Optional thinking mode (same toggle pattern as Qwen3) replaces the need for a separate R-series model. Multimodal support added April 29, 2026. MIT licence.

V4-Flash at Q4_K_M is approximately ~170 GB — still multi-GPU territory.

**V4 benchmark scores:**

| Benchmark | Score |
|-----------|-------|
| MATH-500 | 88.3% |
| HMMT 2026 | 95.2% |
| SWE-Bench Verified | 91.2% |
| GPQA Diamond | 90.1% |
| MMLU-Pro | 87.5% |

### DeepSeek V3.x (2025) — previous generation

| Model | Type | Active / Total | Context | Notes |
|-------|------|---------------|---------|-------|
| DeepSeek-V3 | MoE | 37B / 671B | 128K | Original (Dec 2024) |
| DeepSeek-V3-0324 | MoE | 37B / 671B | 128K | March 2025 weight update |
| DeepSeek-V3.1 | MoE | 37B / 671B | 128K | Aug 2025; adds hybrid thinking mode |
| DeepSeek-V3.2 | MoE | ~37B / 685B | 160K | Dec 2025; DeepSeek Sparse Attention, thinking-in-tool-use |

V3.x GGUF Q4_K_M: ~404 GB — multi-node. Not practical for local inference.

---

## R-series — reasoning (MoE)

| Model | Type | Active / Total | Context | Notes |
|-------|------|---------------|---------|-------|
| DeepSeek-R1 | MoE | 37B / 671B | 128K | Pure chain-of-thought reasoning |
| DeepSeek-R1-0528 | MoE | 37B / 671B | 128K | Updated weights; stronger reasoning |

!!! note "R-series API retirement"
    DeepSeek is retiring the `deepseek-reasoner` API endpoint July 24, 2026. Open weights remain available. V4's built-in thinking mode covers the same use case going forward.

The full R1 requires ~404 GB at Q4_K_M — multi-node territory.

---

## R1 Distills — dense, consumer-friendly

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
| V3.x / V4 (cloud/multi-GPU) | Fast general-purpose chat; hybrid reasoning + general |

**R1 distills are particularly strong at:**
- Mathematical proofs and STEM problem solving
- Code generation and debugging
- Structured logical reasoning
- Tasks benefiting from visible thinking (the `<think>` trace is inspectable)

!!! tip "Best local pick"
    `R1-Distill-Qwen-32B` at Q4_K_M on a 24 GB GPU (e.g., RTX 4090) is the community sweet spot: frontier-class reasoning without multi-GPU requirements.

---

## Source & licence

- **V4 / R1 / distills**: MIT licence
- **V3 originals**: DeepSeek Model Licence (V3.1 and earlier)
- **GGUF models**: search `bartowski/DeepSeek` or `unsloth/DeepSeek` on [huggingface.co](https://huggingface.co)
