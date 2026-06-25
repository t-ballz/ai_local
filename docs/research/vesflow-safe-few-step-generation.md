# VESFlow: Safe Few-Step Generation via Velocity Editing

> Source: [arXiv:2606.23267](https://arxiv.org/abs/2606.23267) · Jun 2026  
> Authors: Yujin Choi, Jaehong Yoon

## TL;DR

VESFlow is a training-free safety method for flow matching text-to-image models that works in the few-step regime (as few as 4–8 steps). By editing velocity fields directly through a safe-conditional posterior, it steers generation away from unsafe content without prompt manipulation or iterative trajectory adjustments. VESFlow+ additionally repels trajectories from unsafe directions, cutting attack success rates to ~6–7%.

---

## The problem

Safety filtering for fast text-to-image models is harder than for full-step models:

1. **Few-step sampling** (4–8 NFEs) leaves little room for iterative trajectory correction — methods that work over 50 steps fail here
2. **Prompt embedding manipulation** (negative prompts, steering vectors) is fragile — adversarial prompts bypass it
3. **Post-hoc filtering** (classifier on output image) can be defeated by prompts that produce unsafe content without explicit keywords

A safety method that works natively at the velocity field level, without retraining, and without depending on prompt content, would be robust across all these attack vectors.

---

## How it works

**Velocity field editing**: In flow matching, generation is a trajectory in latent space guided by a learned velocity field. VESFlow modifies the velocity field at inference time through a *safe-conditional posterior* — a conditional distribution that redirects trajectories toward safe manifolds.

**No training required**: The safe-conditional posterior is derived analytically from a safety classifier's gradients, not learned from scratch.

**VESFlow+**: An enhanced variant that additionally pushes trajectories *away* from unsafe directions (not just toward safe ones), providing a stronger safety signal.

---

## Results

| Method | Attack success rate (lower = safer) |
|---|---|
| Unfiltered | ~80–90% |
| VESFlow | ~6–7% |
| VESFlow+ | ~6–7% with better benign preservation |

Generation quality for benign prompts is maintained — the velocity editing is conditional on safety signals, not applied unconditionally.

---

## Why it matters for local AI

Few-step flow models (FLUX-schnell, Hyper-FLUX) are the practical choice for local image generation — full 50-step inference is too slow on consumer GPUs. VESFlow brings robust safety filtering to the fast generation regime without retraining the base model, making it practical to deploy safe local image generation pipelines.

---

## Limitations

- Safety classifier quality determines the safety guarantee — a weak classifier produces weak safety
- Velocity editing adds a small computational overhead per step (classifier gradient evaluation)
- Evaluated on standard NSFW benchmark datasets; novel adversarial prompts outside this distribution may still succeed

---

## Source

- **Paper**: [arXiv:2606.23267](https://arxiv.org/abs/2606.23267)
- **Preprint date**: Jun 2026
