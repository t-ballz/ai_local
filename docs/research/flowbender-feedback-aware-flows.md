# FlowBender: Feedback-Aware Training for Self-Correcting Conditional Flows

> Source: [arXiv:2606.20404](https://arxiv.org/abs/2606.20404) · June 2026  
> Authors: Daniel Gilo, Sven Elflein, Ido Sobol, Or Litany

## TL;DR

Conditional diffusion and flow models often fail to satisfy their defining constraints at inference time — e.g., a depth-conditioned image model produces outputs whose extracted depth contradicts the input. **FlowBender** is a closed-loop training framework that teaches models to self-correct by providing inference-time alignment feedback. The method alternates between initial unguided generation and refinement steps that use constraint violations as correction signals, improving both fidelity and constraint satisfaction simultaneously.

---

## The problem

Conditional diffusion and flow models are designed to respect constraints (e.g., "generate an image with this depth map," "restore an image under these blur characteristics"). In practice, they often violate these constraints — the generated output, when fed through the forward operator, produces a constraint value that contradicts the condition.

This happens because training typically supervises the model to match data distributions without explicit enforcement of constraint alignment. At inference time, there's no mechanism to detect and correct constraint violations.

---

## Closed-loop training via feedback

FlowBender reframes training as a closed-loop problem. The method operates in two phases per training step:

1. **Unguided generation**: The model generates a candidate sample from a noisy initial state.
2. **Feedback and refinement**: The forward operator evaluates the candidate (e.g., "what depth does this image actually have?"), computes the alignment error, and the model learns to refine the sample using this error signal.

This mirrors inference-time behavior: the model doesn't just learn to match data, it learns a *correction policy* conditioned on real constraint violations.

### Gradient-based and zero-order variants

- **Gradient-based**: For differentiable operators (e.g., edge detection), the framework directly uses gradients of the constraint error.
- **Zero-order**: For non-differentiable operators (e.g., JPEG compression, perceptual metrics), the framework estimates correction without explicit gradients.

Both variants integrate seamlessly into the same training loop.

---

## Key results

Evaluated across three application domains:

- **Image-to-image translation**: Depth-conditioned image generation, edge-conditioned synthesis — FlowBender improves both fidelity (LPIPS, FID) and constraint satisfaction simultaneously.
- **Image restoration**: Denoising and deblurring with explicit constraint targets — models learn to satisfy restoration criteria while maintaining visual quality.
- **3D mesh texturing**: Geometric and lighting constraints — the method extends beyond 2D vision tasks, showing generality.

In all cases, improvements come without the typical trade-off between sample quality and constraint satisfaction; the closed-loop approach achieves both.

---

## Why it matters

Most conditional generation models treat constraints as training signal only — they assume that fitting the data distribution automatically respects the condition. FlowBender flips this: it makes constraint satisfaction an explicit, feedback-driven objective during training itself. This is particularly valuable for applications where constraint violations are costly (robotics, medical imaging, CAD, layout generation).

The framework is agnostic to the specific constraint type and operator, opening a clear path to applications beyond vision (3D generation, control, structured prediction).

---

## Source

- **Paper**: [arXiv:2606.20404](https://arxiv.org/abs/2606.20404)
