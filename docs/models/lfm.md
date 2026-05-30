# LFM (Liquid Foundation Models)

> Source: [liquid.ai](https://www.liquid.ai/blog/lfm2-5-8b-a1b) · [github.com/LiquidAI](https://github.com/LiquidAI) · [HuggingFace LiquidAI](https://huggingface.co/LiquidAI)

## TL;DR

Liquid AI's open-weight model family. Unlike every other model in this wiki, LFM is **not a pure Transformer** — it uses a hybrid architecture combining sparse MoE layers with gated convolution blocks. Current generation: **LFM2.5** (May 2026), featuring an 8B-A1B model with 128K context, strong agentic performance, and a ~5 GB Q4_K_M footprint. Proprietary lfm1.0 licence (free for most uses).

---

## LFM2.5 (May 2026) — current generation

| Model | Type | Active / Total | Context | GGUF Q4_K_M | Notes |
|-------|------|---------------|---------|------------|-------|
| LFM2.5-8B-A1B | Hybrid MoE | 1.5B / 8.3B | 128K | 5.16 GB | CoT reasoning; agentic |

Released May 28, 2026. Trained on 38 trillion tokens.

---

## Architecture

LFM2.5 is a **hybrid sparse model**, not a decoder-only Transformer. Each forward pass routes through 24 layers split into two types:

| Layer type | Count | Role |
|-----------|-------|------|
| LIV convolution (double-gated) | 18 | Sequence mixing via gated short convolutions |
| GQA attention | 6 | Standard grouped-query attention |

The **MoE sparsity** sits in the FFN blocks: 8.3B total parameters, ~1.5B active per token (~18% utilisation). Vocabulary is 128K tokens (doubled from LFM2 to improve non-Latin script coverage).

!!! note "Why this matters for local inference"
    The convolution-heavy design has lower memory bandwidth requirements than an attention-only model of the same active-parameter count. On-device performance is a stated design goal — Apple M5 Max achieves ~253 tokens/sec.

---

## Benchmarks (LFM2.5-8B-A1B)

| Benchmark | Score | Notes |
|-----------|-------|-------|
| MATH500 | 88.76% | Math word problems |
| AIME 2025 | 42.53% | Competition math |
| HumanEval+ | 69.5% | Code generation |
| IFEval | 91.84% | Instruction following |
| GPQA Diamond | 34.4% | Graduate-level science |
| GSM8K | 84.38% | Grade school math |
| MMLU | 64.84% | General knowledge |

Key improvement vs LFM2: hallucination rate down 56 points on the AA-Omniscience index (−24.70 vs −78.42).

---

## Strengths & use cases

| Use case | Notes |
|----------|-------|
| On-device / laptop | Q4_K_M fits in ~6 GB RAM; runs on Apple Silicon and mid-range GPUs |
| Agentic workflows | Explicit chain-of-thought; strong tool-calling and structured output |
| Instruction following | 91.84% IFEval — near the top of sub-10B models |
| Fast inference | 18.5K output tokens/sec on H100; efficient at 1.5B active params |

**Supported inference frameworks**: llama.cpp, Ollama, LM Studio, MLX, vLLM, SGLang, ONNX, Transformers.

---

## GGUF sizes (LFM2.5-8B-A1B)

| Quant | Size |
|-------|------|
| Q4_0 | 4.84 GB |
| Q4_K_M | 5.16 GB |
| Q5_K_M | 6.03 GB |
| Q6_K | 6.96 GB |
| Q8_0 | 9.01 GB |
| BF16 | 16.9 GB |

```bash
# Ollama
ollama pull lfm2.5:8b

# llama.cpp / direct download
# huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF
```

---

## Generation history

| Generation | Release | Context | Training tokens | Key change |
|-----------|---------|---------|-----------------|------------|
| LFM2-8B-A1B | 2025 | 32K | 12T | Initial hybrid MoE |
| LFM2.5-8B-A1B | May 2026 | 128K | 38T | CoT, 128K vocab, lower hallucination |

---

## Source & licence

- **Source**: [huggingface.co/LiquidAI](https://huggingface.co/LiquidAI)
- **Licence**: lfm1.0 (Liquid AI proprietary; free for research and commercial use under stated terms — check [liquid.ai/legal](https://www.liquid.ai/legal) for details)
- **GGUF models**: [huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF](https://huggingface.co/LiquidAI/LFM2.5-8B-A1B-GGUF)
