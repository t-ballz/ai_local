# LFM (Liquid Foundation Models)

> Source: [liquid.ai](https://www.liquid.ai/blog/lfm2-5-8b-a1b) · [github.com/LiquidAI](https://github.com/LiquidAI) · [HuggingFace LiquidAI](https://huggingface.co/LiquidAI)

## TL;DR

Liquid AI's open-weight model family. Unlike every other model in this wiki, LFM is **not a pure Transformer** — it uses a hybrid architecture combining sparse MoE layers with gated convolution blocks. Current generation: **LFM2.5** (2026), featuring a text-only 8B-A1B (May 2026, 128K context, ~5 GB Q4_K_M) and two vision-language variants — VL-1.6B (Jan 2026) and VL-450M (Apr 2026, bounding box prediction, <250ms on edge). Proprietary lfm1.0 licence (free for most uses).

---

## LFM2.5 (May 2026) — current generation

| Model | Type | Active / Total | Context | GGUF Q4_K_M | Notes |
|-------|------|---------------|---------|------------|-------|
| LFM2.5-8B-A1B | Hybrid MoE | 1.5B / 8.3B | 128K | 5.16 GB | CoT reasoning; agentic |

Released May 28, 2026. Trained on 38 trillion tokens.

---

## LFM2.5 Vision-Language variants

Two dedicated VLMs alongside the text-only 8B-A1B — purpose-built with a SigLIP2 vision encoder paired to a smaller LFM2.5 language backbone, rather than a multimodal extension of the 8B.

| Model | LM backbone | Vision encoder | Context | Formats | Released |
|-------|------------|---------------|---------|---------|---------|
| LFM2.5-VL-1.6B | LFM2.5-1.2B | SigLIP2 NaFlex 400M | 32K | GGUF / ONNX / MLX | Jan 2026 |
| LFM2.5-VL-450M | LFM2.5-350M | SigLIP2 Base 86M | 32K | GGUF | Apr 2026 |

Both handle 512×512 images natively; larger images are tiled into non-overlapping 512×512 patches. Both support multilingual vision (Arabic, Chinese, French, German, Japanese, Korean, Spanish).

### LFM2.5-VL-1.6B

Focuses on document understanding, high-resolution OCR, and multi-image reasoning.

| Benchmark | Score |
|-----------|-------|
| RealWorldQA | 64.84 |
| MMStar | 50.67 |
| MM-IFEval | 52.29 |
| OCRBench | 41.44 |

```python
from transformers import AutoModelForImageTextToText
model = AutoModelForImageTextToText.from_pretrained(
    "LiquidAI/LFM2.5-VL-1.6B", device_map="auto", dtype="bfloat16"
)
```

Supported runtimes: HF Transformers (≥5.1), vLLM, llama.cpp, SGLang, ONNX, MLX.

### LFM2.5-VL-450M

Smaller edge variant. Adds **bounding box prediction** (grounded visual understanding) and function calling. Sub-250ms on Jetson Orin.

**Edge latency (Q4_0, inference):**

| Device | Resolution | Latency |
|--------|-----------|---------|
| NVIDIA Jetson Orin | 512×512 | 242 ms |
| Samsung S25 Ultra | 256×256 | 950 ms |
| AMD Ryzen AI Max+ 395 | 512×512 | 944 ms |

**Benchmarks vs predecessor LFM2-VL-450M:**

| Benchmark | LFM2 | LFM2.5 |
|-----------|------|--------|
| RefCOCO-M (bounding box) | 0 | **81.28** |
| MMMB (multilingual vision) | 54.29 | 68.09 |
| IFEval | 51.75 | 61.16 |
| MMBench | — | 60.91 |
| OCRBench | — | 684 |

**GGUF**: `LiquidAI/LFM2.5-VL-450M-GGUF` on HuggingFace.

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
