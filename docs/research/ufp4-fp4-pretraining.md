# UFP4: Fixing 4-bit Floating Point Pretraining with Uniform Grids

> Source: [arXiv:2606.20381](https://arxiv.org/abs/2606.20381) · June 2026  
> Authors: Qian Zhao, Kunlong Chen, Changxin Tian, Zhonghui Jiang, Haitao Zhang, Chaofan Yu, Peijie Jiang, Mingliang Gong, Jia Liu, Ziqi Liu, Zhiqiang Zhang, Jun Zhou

## TL;DR

FP4 (4-bit floating point) training could slash LLM pretraining compute, but popular non-uniform formats like E2M1 suffer from **shrinkage bias** — systematic rounding errors from geometric asymmetry in their number grids. UFP4 fixes this by switching to uniform formats (E1M2/INT4), consistently improving loss degradation across model scales from 1.5B to 124B parameters.

---

## The problem

FP4 pretraining is appealing: 4 bits instead of 16 could reduce memory, bandwidth, and compute costs dramatically. But when researchers began using non-uniform formats like E2M1 in actual training, something went wrong.

**Shrinkage bias** is the culprit: a "systematic negative rounding error caused by the geometric asymmetry of their representable bins." The problem emerges because E2M1 and similar non-uniform formats don't distribute numbers evenly. Some regions of the number line are densely packed; others are sparse. When gradients and activations get rounded to the nearest representable value, they cluster towards certain values — systematically undershooting the true magnitude.

This wouldn't be a big deal if it happened once. But:
- It compounds across layers as data flows through the network
- It's amplified by Random Hadamard Transform (RHT), a technique used to improve numerical precision in low-bit arithmetic
- Small-scale experiments miss it; the effect scales with model size

---

## Root cause: Geometric asymmetry

The core insight is geometric. Non-uniform formats like E2M1 don't have evenly-spaced representable values:

- **E2M1** (2 exponent bits, 1 mantissa bit) clusters some values tightly and leaves gaps elsewhere
- **Uniform formats** like E1M2 and INT4 spread representable values evenly across the range they cover

When you round a value to the nearest representable point in a non-uniform grid, the average rounding error is biased — it pulls you slightly downward, not toward the true value. Over millions of gradient updates, this "shrinkage" accumulates, inflating loss and degrading final model quality.

---

## UFP4 recipe: E1M2 and INT4 grids

The paper proposes UFP4: a training approach that uses **uniform 4-bit formats exclusively**:

1. **E1M2 format**: 1 exponent bit, 2 mantissa bits — simple, uniform grid
2. **INT4 format**: Integer representation where applicable — also uniform
3. **Random Hadamard Transform on all three GEMMs**: Apply RHT during weight-gradient products, activation-gradient products, and gradient products. RHT helps decorrelate data for better quantization.
4. **Stochastic rounding for gradients only**: Rather than rounding all computations, use probabilistic rounding specifically in gradient computations to reduce bias further

This is deliberately conservative: it standardizes on uniform grids everywhere and applies stochastic rounding surgically where it helps most.

---

## Results

### Model scales tested
- **Dense:** 1.5B parameters
- **Mixture of Experts (MoE):** 7.9B and 124B parameters

### Key findings

**UFP4 achieves lower BF16-relative loss degradation than strong E2M1-based baselines** across all three scales. In other words: if you train the same model in BF16 (the "ground truth"), then measure how much worse it performs in UFP4 vs. E2M1, UFP4 wins.

The improvements are consistent and scale-independent — neither tiny models nor giant MoE systems exploit the uniform grid assumption in a way that breaks the approach.

### Validation

The results come with rigorous supporting analysis:
- **Scaling laws** show the trend holds as models grow
- **Ablation studies** isolate which components of UFP4 matter (RHT placement, stochastic rounding scope)
- **Comparisons to baselines** include the current best non-uniform approaches

---

## Why it matters

### Compute efficiency for LLM pretraining

FP4 training could unlock orders of magnitude of speedup. If you can reduce from FP32/BF16 (16 bits) to FP4 (4 bits), you halve memory bandwidth and storage. But shrinkage bias meant this wasn't working in practice — models trained in E2M1 lost quality, forcing researchers back to wider formats.

UFP4 removes that obstacle. By demonstrating that uniform grids consistently work, it makes a case to hardware vendors: **build accelerators that prioritize uniform 4-bit arithmetic as a training primitive, not an afterthought.**

### Implications for hardware

The paper explicitly recommends:
> "Future accelerators should prioritize uniform 4-bit grids as training primitives"

This is important because it reframes what hardware teams should invest in. Instead of optimizing E2M1 or other non-uniform formats, focus on E1M2 and INT4. Uniform grids are simpler to implement, easier to reason about, and empirically superior.

### Systemic risk of ad-hoc formats

Non-uniform quantization formats are seductive because they look like they'd preserve more precision. But the paper shows the opposite: **the "precision" they offer comes with systematic bias that is worse than the loss from uniform quantization.** This is a reminder that in numerical computing, symmetry and uniformity often beat raw precision.

---

## Limitations & open questions

The paper doesn't address:
- Mixed-precision strategies (when to use E1M2 vs INT4 in the same network)
- Communication efficiency during distributed training with 4-bit gradients
- How shrinkage bias behaves with other quantization methods (post-training quantization, inference-only quantization)

---

## Source

- **Paper**: [arXiv:2606.20381](https://arxiv.org/abs/2606.20381)
- **Preprint date**: June 18, 2026
