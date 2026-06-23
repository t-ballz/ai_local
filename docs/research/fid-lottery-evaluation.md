# FID Scores Hide a Randomness Tax — And It's Costing Billions in Wasted Compute

> Source: [arXiv:2606.20536](https://arxiv.org/abs/2606.20536) · June 2026  
> Authors: Nicolas Dufour, Alexei A. Efros, Patrick Pérez

## TL;DR

FID (Fréchet Inception Distance), the standard metric for evaluating generative image models, has a hidden 1-2% coefficient of variation from random seeds. Lucky training seeds achieve the same quality with 2× less compute than unlucky ones — yet this variability is systematically hidden from results. The paper proposes mandatory error bars over multiple training seeds as an evaluation standard.

---

## The problem

FID is the canonical metric for measuring generative image quality. It's in almost every paper. But there's a dirty secret: **two identical models trained with different random seeds can have substantially different FID scores**.

This randomness comes from three sources:
1. **Random initialization** — weight initialization varies between runs
2. **Data ordering** — the order in which training examples are seen affects gradient flow
3. **Noise in the training process** — stochastic elements like dropout and Gaussian noise in loss functions

The problem isn't that randomness exists — it's that researchers report a single FID number and pretend it's the truth. In reality, that number is just one draw from a distribution.

---

## What the paper found

### Coefficient of variation: ~1.3% is the noise floor

Across multiple experiments, the "FID coefficient of variation remains within a 1-2% band." This means:
- If a model achieves FID = 5.0, the true central estimate is probably 5.0 ± 0.065–0.1
- Differences smaller than ~1.3% CoV are indistinguishable from noise
- Claiming one training run is "better" than another based on a 1% FID difference is meaningless

### The compute lottery: 2× difference from seed selection

A particularly fortunate seed can "reach the same FID with up to 2x less compute than an unlucky one." This is not marginal. In a field where training a single large diffusion model costs thousands of dollars, seed selection can be the difference between a publishable result and one that requires weeks more training.

### Retraining variance dominates resampling variance

The paper measured two sources of variation:
- **Retraining variance** (different random seeds, same architecture/data)
- **Resampling variance** (same trained model, different random samples during inference)

Retraining produces "3.2x more" variation than resampling. This means **the randomness in the training process, not the sampling process, is the dominant source of FID variability**.

---

## Proposed fix: Mandatory error bars

The authors recommend:
1. **Report error bars over multiple training seeds** rather than a single FID number
2. **Treat gaps below ~1.3% CoV as inconclusive** — don't claim an improvement if it falls within the noise floor
3. **Use per-cell optimal guidance** for diffusion model evaluation (a technical detail for ensuring fair comparison)

This is a simple protocol that would instantly make generative model papers more rigorous and reproducible.

---

## Why it matters

### Reproducibility crisis disguised as precision
Current practice creates an illusion of precision. A paper reports "FID = 4.87" and the next paper claims "4.73, which is better." But if the true uncertainty is ±0.1, both claims are the same model.

### Hiding failed experiments
If a researcher trains a model 10 times and gets FID scores of [5.0, 4.9, 4.8, 5.1, 5.2, 4.7, 5.3, 5.1, 4.8, 4.9], they might report the minimum (4.7) as their "best result" and not mention the others. This is publication bias in the raw data. The honest report would be "FID = 5.0 ± 0.18."

### Implications for compute efficiency
The 2× compute lottery means researchers may unknowingly be comparing apples (lucky seed) to oranges (unlucky seed) when claiming a new method is "more efficient." A fair comparison requires running multiple seeds for both baselines and proposed methods.

### Standards for model comparison
The proposed 1.3% CoV threshold provides a clear, principled way to judge whether a claimed improvement is real:
- **>1.3% difference**: Likely real improvement (if measured properly over multiple seeds)
- **<1.3% difference**: Inconclusive; need more evidence

---

## Implications for the field

1. **New papers should report error bars** — FID without uncertainty estimates should become unacceptable, just as raw p-values without confidence intervals are questioned in statistics.

2. **Retraining reproducibility matters more than inference randomness** — if you want reproducible evaluations, control the training procedure, not just the sampling.

3. **Lucky seeds inflate perceived efficiency** — claims about "2× faster training" or "better quality at lower compute" need to account for seed variation. The best baseline might just be unlucky.

4. **Existing leaderboards are unreliable** — comparing papers that used single seeds makes no sense. Historical results should be re-evaluated with error bars.

---

## Source

- **Paper**: [arXiv:2606.20536](https://arxiv.org/abs/2606.20536)
