# Moebius: Lightweight Image Inpainting Framework

> Source: [arXiv:2606.19195](https://arxiv.org/abs/2606.19195) · June 2026  
> Authors: Kangsheng Duan, Ziyang Xu, Wenyu Liu, Xiaohu Ruan, Xiaoxin Chen, Xinggang Wang

## TL;DR

Moebius is a 0.22B image inpainting model that matches 10B-class performance through Local-λ Mix Interaction (LλMI) blocks and adaptive multi-granularity distillation. It runs **15× faster** than FLUX.1-Fill-Dev while using less than 2% of its parameters, with competitive or superior generation quality on natural and portrait inpainting benchmarks.

---

## The problem

Large diffusion-based inpainting models like FLUX.1-Fill-Dev (11.9B parameters) are computationally expensive and impractical for many deployment scenarios. Standard approaches to compress these models—parameter pruning, quantization, knowledge distillation—either lose significant quality or require expensive pixel-space supervision during training.

---

## Local-λ Mix Interaction (LλMI) blocks

Instead of operating on full spatial feature maps, LλMI blocks summarize spatial contexts and global semantic priors into **fixed-size linear matrices**. This reduces the parameter cost while maintaining latent interactions between local regions and global information through efficient mixing operations.

The key insight: inpainting doesn't require dense spatial computation at full resolution. By compressing spatial context into learned summaries, the model can preserve semantic coherence while dramatically reducing parameters.

---

## Adaptive multi-granularity distillation

Rather than distilling in pixel space (which is expensive), Moebius performs distillation in the **latent space** with adaptive granularity. This means:

- Coarse granularity captures overall semantic structure
- Fine granularity refines details where the student model struggles most
- Granularity adapts based on per-sample distillation difficulty

This strategy aligns the student model with the teacher's high-quality generations without the computational cost of decoding to images during training.

---

## Key results

| Metric | Value |
|--------|-------|
| Model size | 0.22B parameters (vs. 11.9B baseline) |
| Parameter reduction | 98% fewer parameters |
| Inference speedup | 15× faster than FLUX.1-Fill-Dev |
| Performance | Competitive or superior on natural and portrait benchmarks |
| Availability | Open weights on HuggingFace |

---

## Why it matters

- **Deployment**: Moebius enables real-time image inpainting on edge devices and consumer hardware without sacrificing quality
- **Efficiency benchmark**: Demonstrates that modern diffusion models can be compressed far more aggressively than previously thought — 98% parameter reduction with quality preservation is unprecedented at this scale
- **Distillation innovation**: Adaptive latent-space distillation is a reusable technique for compressing other diffusion-based generative models
- **Open weights**: Unlike FLUX.1-Fill-Dev, Moebius is fully open-source, enabling research and customization

---

## Source

- **Paper**: [arXiv:2606.19195](https://arxiv.org/abs/2606.19195)
