# PerceptionDLM: Parallel Region Perception with Multimodal Diffusion Language Models

> Source: [arXiv:2606.19534](https://arxiv.org/abs/2606.19534)  
> Authors: Yueyi Sun, Yuhao Wang, Jason Li, Ye Tian, Tao Zhang, Jacky Mai, Yihan Wang, Haochen Wang, Jinbin Bai, Ling Yang, Yunhai Tong  
> Code: [MSALab-PKU/PerceptionDLM](https://github.com/MSALab-PKU/PerceptionDLM)

## TL;DR

PerceptionDLM extends LLaDA-8B (an open-weight masked diffusion language model) with **region-aware prompting** and **structured attention masking** to caption multiple image regions in a single parallel inference pass. A new benchmark, ParaDLC-Bench, evaluates multi-region caption generation quality and inference efficiency, demonstrating substantial speedups over sequential region captioning.

---

## The multi-region captioning bottleneck

Existing multimodal LLMs handle region captioning by processing one region at a time — requiring N separate forward passes for N regions. This is inefficient even though the underlying task (describing different spatial patches of the same image) should be parallelizable.

PerceptionDLM solves this by:
1. **Encoding multiple region queries in a single prompt** with per-region positional/visual anchors
2. **Masking token generation** so each region's caption is generated independently within the diffusion process
3. **Parallel inference** — all regions decoded in one pass

---

## Architecture

### Foundation: LLaDA-8B

Builds on **LLaDA-8B**, an open-weight masked diffusion language model that:
- Uses diffusion (not autoregression) for token generation
- Supports arbitrary masking patterns during inference
- Enables parallel token prediction across masked positions

### Region-aware prompting

Regions are specified as:
- **Bounding box coordinates** or **mask tokens** embedded in the text prompt
- **Localized visual features** extracted from each region (e.g., CLIP embeddings or visual patches)
- Each region gets its own anchor token in the diffusion conditioning

### Structured attention masking

Instead of shared attention across all tokens, PerceptionDLM uses:
- **Per-region attention masks** that isolate each region's generation path during diffusion sampling
- **Cross-region boundaries** remain decoupled — regions generate independently
- The diffusion process naturally handles iterative refinement at both sequence and token levels

---

## ParaDLC-Bench

A new benchmark extending **DLC-Bench** (Detailed Localized Captioning):
- **Multiple region masks per image** — typical images have 2–5 regions to caption jointly
- **Parallel evaluation** — measures generation quality for all regions in a single forward pass
- **Efficiency metric** — tracks wall-clock time improvement vs. sequential processing
- Baseline: sequential region-by-region captioning; target: PerceptionDLM's parallel approach

---

## Key results

- **Speedup**: Substantial inference time reduction for multi-region tasks vs. sequential captioning
- **Quality**: Competitive region caption quality compared to single-region models
- **Scalability**: Linear scaling with number of regions (avoiding exponential slowdown from sequential processing)
- **Open-weight baseline**: PerceptionDLM-Base released alongside paper (LLaDA-8B + region components)

---

## Why diffusion for this task?

Autoregressive models generate one token at a time — inherently sequential. Diffusion language models (DLMs) naturally support:
- **Masked generation** — only refine a specific subset of positions per diffusion step
- **Independent decoding paths** — regions can diffuse in parallel without explicit gating
- **Flexible masking patterns** — support arbitrary spatial or semantic boundaries without architectural modification

This makes diffusion a natural fit for the parallel, region-decoupled nature of multi-region captioning.

---

## Availability

- **Code & Models**: [github.com/MSALab-PKU/PerceptionDLM](https://github.com/MSALab-PKU/PerceptionDLM)
- **Datasets**: ParaDLC-Bench released alongside the paper
- **Model weights**: PerceptionDLM-Base available for download
