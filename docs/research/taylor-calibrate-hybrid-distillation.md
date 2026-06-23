# Taylor-Calibrate: Principled Initialization for Hybrid Distillation

> Source: [arXiv:2606.16429](https://arxiv.org/abs/2606.16429) · June 2026  
> Authors: Zhongzhu Zhou, Qingyang Wu, Junxiong Wang, Mayank Mishra, Shuaiwen Leon Song, Ben Athiwaratkun, Chenfeng Xu

## TL;DR

Converting full-attention Transformers into hybrid models (mixing full softmax + linear/recurrent attention like GDN) fails without proper initialization of recurrent parameters. Taylor-Calibrate analytically initializes decay gates and other recurrent weights using Taylor expansion of the teacher's attention statistics, cutting training time 4.9–9.2× and achieving 88× improvement in zero-shot performance versus naive conversion.

---

## The Problem

**Hybrid architectures** (e.g., mixing full attention with Gated DeltaNet or Mamba) are efficient, but knowledge distillation is fragile. Simply copying teacher attention projections into a hybrid student doesn't define:
- Recurrent decay timescales (memory retention across tokens)
- Write gates (gating mechanism for state updates)
- Output gates (scaling recurrent outputs)

Result: **training collapses or recovers extremely slowly** from a poor initialization.

---

## Taylor-Calibrate Method

### Core Insight

Use **Taylor expansion** of the teacher's attention statistics to derive closed-form initialization for recurrent parameters.

For each layer, analyze how the teacher attention distributes information across positions, then translate that into equivalent recurrent dynamics:
1. **Compute teacher statistics**: Attention weight distributions, value projections, softmax temperatures
2. **Taylor-expand** attention behavior around the recurrent model's implied update rules
3. **Solve for parameters**: Decay rates, write gate biases, output gate scales
4. **Per-layer alignment**: Fine-tune one layer at a time to match teacher intermediate representations

### Key Innovation

Instead of random initialization or gradient-based tuning from scratch, derive parameters analytically from the teacher's behavior. This is **lightweight** — no full retraining needed.

---

## Results

| Metric | Improvement |
|--------|-------------|
| Zero-shot performance (ablation) | 88× better than naive conversion |
| Training token efficiency | 4.9–9.2× fewer tokens to reach recovery targets |
| Models tested | LLaMA 3.2-3B-Instruct, Qwen 3.5-27B |
| Hybrid architectures | GDN + full attention; tested across 4 teacher settings, 3 retained-layer policies |

The method is agnostic to specific hybrid designs, generalizing across different efficient attention mechanisms (GDN, Mamba-style, etc.).

---

## Cross-Link

See also: [Rethinking Efficient Attention in Hybrid Architectures](efficient-attention-hybrid-architectures.md) — explores how efficient attention layers shape the development of long-range retrieval capabilities in hybrid models.

---

## Why It Matters

Hybrid models are becoming standard (Jamba, Samba, H3, etc.), but distillation from larger teachers has been slow or unreliable. Taylor-Calibrate removes that bottleneck, making it practical to:
- Distill large pretrained models into efficient hybrids
- Rapidly prototype hybrid architectures
- Scale down full-attention models without losing performance
