# DF3DV-1K: Distractor-Free Novel View Synthesis Dataset and Benchmark

> Source: [arXiv:2604.13416](https://arxiv.org/abs/2604.13416) · April 2026  
> Authors: Cheng-You Lu, Yi-Shan Hung, Wei-Ling Chi, Hao-Ping Wang, Charlie Li-Ting Tsai, Yu-Cheng Chang, Yu-Lun Liu, Thomas Do, Chin-Teng Lin

## TL;DR

A 1,048-scene real-world dataset with 89,924 images for benchmarking distractor-free novel view synthesis. Includes clean and cluttered image pairs across 128 distractor types and 161 scene themes. Evaluates radiance field methods and 3D Gaussian Splatting, revealing robustness gaps and enabling distractor-robust model development.

---

## The problem

Recent advances in radiance fields (NeRF variants) have achieved photorealistic novel view synthesis, but **most evaluations focus on clean scenes**. Real-world applications face visual distractors—occlusions, dynamic objects, reflections, semi-transparent elements—that degrade synthesis quality. Prior work on distractor-robust methods lacks a large-scale, systematic benchmark:

- Existing datasets don't provide **clean-and-cluttered pairs** for the same scenes
- No systematic cataloging of distractor types and their effects
- Unclear which methods are robust to which distractors
- No standard evaluation protocol for distractor-free view synthesis

This limits progress toward practical deployments where real-world clutter is unavoidable.

---

## DF3DV-1K Dataset

| Metric | Value |
|--------|-------|
| Total scenes | 1,048 |
| Total images | 89,924 |
| Distractor types | 128 |
| Scene themes | 161 |
| Evaluation subset | DF3DV-41 (41 curated scenes) |
| Environments | Indoor and outdoor |
| Capture device | Consumer cameras (casual capture) |

**Structure**: Each scene provides both clean and cluttered image sets captured from the same viewpoints, enabling direct distractor-impact measurement.

**Distractor coverage**: 128 distractor types span occlusions, dynamic objects, reflections, transparency, clutter, and environmental variations.

**DF3DV-41 subset**: A carefully curated 41-scene evaluation set designed for systematic stress-testing of methods under challenging scenarios.

---

## Benchmark results

The paper evaluates:
- **9 distractor-free radiance field methods** (state-of-the-art approaches optimized for robustness)
- **3D Gaussian Splatting** (modern alternative to NeRF-based approaches)

Key findings:
- Significant performance gaps between methods under distractor presence
- Some methods robust to certain distractor types but vulnerable to others
- Current methods not uniformly robust across the 128 distractor types
- Clear ranking of methods by overall robustness

**Application**: Fine-tuned a diffusion-based 2D enhancer as a preprocessing step for radiance fields, achieving average improvements of **0.96 dB PSNR** and **0.057 LPIPS** on held-out sets (DF3DV-41 and On-the-go dataset).

---

## Why it matters

1. **Closes a benchmarking gap**: First large-scale dataset specifically for distractor-free novel view synthesis, with systematic distractor taxonomy

2. **Enables robustness research**: Clean-cluttered pairs allow isolating distractor effects and developing robust methods

3. **Practical relevance**: Real-world capture inevitably includes distractors; benchmarking against them surfaces real deployment challenges

4. **Method transparency**: Systematic evaluation reveals which methods fail under which conditions, guiding architecture and training improvements

5. **Community progress**: Public dataset and leaderboard accelerate development of distractor-robust radiance fields

---

## Source

- **Paper**: [arXiv:2604.13416](https://arxiv.org/abs/2604.13416)
