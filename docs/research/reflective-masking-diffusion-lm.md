# Reflective Masking: Eliciting Reasoning in Mask Diffusion Models

> Source: [arXiv:2606.16700](https://arxiv.org/abs/2606.16700) · June 2026  
> Authors: Yanming Zhang, Yihan Bian, Jingyuan Qi, Yuguang Yao, Lifu Huang, Tianyi Zhou

## TL;DR

Masked diffusion language models (MDMs) generate text by iteratively denoising random masks — they can refine any token at any position. **Reflective Masking** amplifies this advantage: selectively re-mask tokens the model is uncertain about and re-run the denoising process, creating a form of chain-of-thought reasoning. Training is lightweight (5 hours on 2×H100). Improves code generation (+8.8% on MBPP), math reasoning (+2.4% on MATH500), and image editing (99.7% edit precision).

---

## The Problem: Reasoning in Diffusion LMs

Masked diffusion models generate differently from autoregressive LMs. An autoregressive model produces tokens left-to-right in a fixed sequence; a diffusion model starts with all positions masked and iteratively refines them in arbitrary order. This flexibility enables editing (swap a token without regenerating the rest), but it also lacks the built-in "chain-of-thought" structure that sequential generation provides.

How do you get reasoning behavior out of an order-agnostic denoising process?

---

## Reflective Masking: The Mechanism

### The Core Idea

After each denoising pass, **re-mask tokens where the model is uncertain** and repeat the refinement process. Uncertainty is measured simply: if the model assigns higher probability to MASK than to its own predicted token, that token is re-masked.

Mathematically:
- Re-mask position *i* if: **p(MASK | x̃^(t)) > p(x̃_i^(t) | x̃^(t))**
- Then run another denoising iteration, allowing the model to reconsider.

This creates a multi-turn refinement loop — like asking the model to double-check its work.

### History Reference (HR)

A parameter-free addition: keep track of intermediate denoising states from prior turns and condition on them. The model can leverage what it computed in earlier refinement steps without adding learnable parameters.

### Test-Time Scaling

Unlike autoregressive models, where reasoning is baked in during training, diffusion models can naturally scale reasoning at *inference time*: just run more denoising iterations. Reflective Masking doesn't require architectural changes — it's purely algorithmic.

---

## Results

### Text Reasoning

Evaluated on reasoning benchmarks with a diffusion language model baseline (LLaDA):

| Benchmark | Vanilla SFT | + Reflective Masking | Improvement |
|-----------|------------|---------------------|------------|
| MATH500 | 22.4% | 24.8% | +2.4% |
| MBPP (code) | 30.6% | 39.4% | +8.8% |
| ARC-Challenge | 81.3% | 86.1% | +4.8% |
| Minerva MATH | 22.62% | 24.10% | +1.48% |

The largest gains are on code generation, where selective re-masking helps the model refine implementation details.

### Image Editing (Lumina-DiMOO)

Reflective Masking improves targeted image edits:

- **Edit Precision**: 99.73%
- **Edit Coverage**: 73.02%
- **PSNR**: 34.759 dB
- **SSIM**: 0.9744
- **User Study**: 68.2% preference vs. baseline

Image editing is a natural fit for diffusion: tokens can be refined independently. Reflective Masking's selective re-masking aligns perfectly with the task.

### Sudoku Solving

On Sudoku revision tasks (filling in blanks while preserving constraints):

- **Exact Accuracy**: 93.4%
- **Valid Rate**: 93.6%
- **Replay Mistake Rate**: 0.03%

---

## Comparison to Autoregressive Chain-of-Thought

| Aspect | Autoregressive CoT | Reflective Masking |
|--------|-------------------|-------------------|
| Generation order | Fixed (left-to-right) | Flexible, any order |
| Reasoning | Baked into sequence during training | Applied at test time |
| Compute | Linear in sequence length + CoT steps | Denoising iterations |
| Editing | Requires full regeneration | Direct token refinement |
| Scaling | Requires retraining for different CoT depths | Scales naturally with iterations |

Reflective Masking is not sequential reasoning — it's **iterative refinement reasoning**. The model reconsiders uncertain positions given improved context from other positions. This is native to diffusion; autoregressive models must simulate it through token-by-token generation.

---

## Training & Compute

- **Training time**: ~5 hours on 2 NVIDIA H100 80GB GPUs
- **Method**: Post-training (applied after SFT)
- **Lightweight**: No architectural changes; purely algorithmic

The training burden is minimal because Reflective Masking requires only supervised examples of multi-turn refinement — no RLHF, no complex reward modeling.

---

## Why It Matters

This is the diffusion LM equivalent of chain-of-thought prompting for autoregressive models. While [d-OPSD](dopsd-diffusion-llm-distillation.md) focuses on *self-improvement training* for diffusion LMs, Reflective Masking is a *reasoning mechanism* — two complementary approaches to making diffusion LMs more capable.

Together, they demonstrate that diffusion language models are a viable alternative to autoregressive generation, with their own strengths: better editability, flexible refinement order, and native test-time scaling.

---

## Source

- **Paper**: [arXiv:2606.16700](https://arxiv.org/abs/2606.16700)
- **Project page**: Mentioned in paper (check for code/model releases)
