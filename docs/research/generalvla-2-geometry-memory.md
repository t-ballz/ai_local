# GeneralVLA-2: Geometry-Aware Reconstruction and Governed Memory for Robot Planning

> Source: [arXiv:2606.17480](https://arxiv.org/abs/2606.17480) · Jun 2026  
> Authors: Haoyu Wang, Guoqing Ma, Zeyu Zhang, Yandong Guo, Boxin Shi, Hao Tang

## TL;DR

GeneralVLA-2 extends the GeneralVLA vision-language-action model with two improvements: GeoFuse-MV3D for geometry-aware 3D object reconstruction from monocular views, and a governed memory system that tracks quality, confidence, and conflict metadata. Together they improve 3D reconstruction quality and downstream task success rates, with code and weights publicly available.

---

## The problem

VLA models for robot manipulation need accurate 3D object understanding and reusable experience. Two gaps in the original GeneralVLA:

1. **Monocular reconstruction** is unreliable — single-view depth estimation fails on occluded or partially visible objects, leading to planning errors
2. **Memory systems** (like the original KnowledgeBank) lack quality tracking — old or conflicting memories can degrade planning rather than helping it

---

## How it works

**GeoFuse-MV3D**: Tackles single-view reconstruction limits by incorporating multi-view geometry priors:
- Verifies external geometry cues against input-view masks
- Applies soft visual-hull constraints to prune implausible reconstructions
- Performs axis-wise refinement to correct systematic biases
- Fuses geometric data with appearance information for final output

**Governed Memory System**: Replaces the original KnowledgeBank with explicit metadata tracking per memory entry:
- Quality score
- Confidence estimate
- Lifecycle (age, access frequency)
- Verifier (who/what added this memory)
- Conflict resolution metadata

Precision-focused retrieval uses this metadata to surface high-confidence, non-conflicting memories rather than naively retrieving by recency or similarity.

---

## Results

| Component | Metric | Improvement |
|---|---|---|
| GeoFuse-MV3D | CD (Chamfer Distance) | −2.20% |
| GeoFuse-MV3D | LPIPS | −2.02% |
| GeoFuse-MV3D | PSNR | +2.36% |
| GeoFuse-MV3D | SSIM | +1.03% |
| Governed Memory | Terminal-Bench SR | +4.53% |
| Governed Memory | SWE-Bench resolve rate | +3.73% |
| Governed Memory | Action steps | −4.95% to −5.65% |

---

## Why it matters for local AI

- **Open weights**: Code and model weights are publicly available — directly usable for robotics research
- **GeoFuse-MV3D pattern**: The multi-view geometry verification approach is applicable to any 3D perception task beyond robotics (scene reconstruction, AR, spatial AI)
- **Governed memory**: The metadata-driven memory system is a practical pattern for any long-running agent that accumulates experience over time — not just robots

---

## Limitations

- Improvements are incremental (2–5%) rather than transformative
- Multi-view reconstruction requires multiple camera views at inference — single-camera setups can't fully exploit GeoFuse-MV3D
- Terminal-Bench and SWE-Bench are coding/planning benchmarks; real-world physical robot results not reported in the abstract

---

## Source

- **Paper**: [arXiv:2606.17480](https://arxiv.org/abs/2606.17480)
- **Preprint date**: Jun 2026
