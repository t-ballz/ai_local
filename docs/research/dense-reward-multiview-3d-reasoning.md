# DR-MV3D: Dense Reward for Multi-View 3D Visual Reasoning

> Source: [arXiv:2606.23557](https://arxiv.org/abs/2606.23557) · Jun 2026  
> Authors: Jiho Choi, Seonho Lee, Seojeong Park, Hyunjung Shim

## TL;DR

DR-MV3D addresses Multi-View 3D VQA by decomposing the task into global map construction, question-conditioned view-trajectory planning, and egocentric grounding, then training with dense rewards at each stage rather than answer-level supervision only. Consistent improvements over multi-image baselines on MindCube, VSI-Bench, and BLINK.

---

## The problem

Multi-view 3D Visual Question Answering — answering questions about a scene from multiple camera viewpoints — requires spatial reasoning that goes beyond single-image VLMs. Current approaches either:

1. Flatten all views into a single long image sequence (losing spatial structure)
2. Rely on answer-level supervision only (can't tell the model *where* its spatial reasoning broke down)

The result is brittle 3D reasoning that struggles to localize objects, estimate distances, or track spatial relationships across views.

---

## How it works

**Three-stage pipeline**:

1. **Allocentric global map construction**: Build a bird's-eye-view map of the scene from all available views. This is the scene-level representation — object positions, spatial layout.

2. **Question-conditioned view-trajectory planning**: Given the question, plan a sequence of viewpoints to inspect for answering it. Not all views are equally relevant — this stage selects the informative ones.

3. **Egocentric grounding**: From the selected viewpoints, ground the answer in specific visual evidence.

**Dense reward training**:
- **Global consistency reward**: Validates the predicted map against geometry-based targets from frozen 3D vision models (not the answer) — provides supervision on spatial map quality independently of the final answer
- **Local trajectory reward**: Rewards selecting viewpoints that are informative for the specific question
- **Trajectory-level policy optimization**: The full pipeline is optimized end-to-end using these intermediate rewards

---

## Results

| Benchmark | Improvement |
|---|---|
| MindCube | Consistent improvement over multi-image baselines |
| VSI-Bench | Consistent improvement |
| BLINK | Consistent improvement |

---

## Why it matters for local AI

3D spatial reasoning from multiple camera views is a core capability for robot navigation, AR/VR agents, and embodied systems. DR-MV3D's dense reward approach — providing training signal at the map quality and view selection stages, not just the final answer — is a general pattern for decomposing complex multi-step visual tasks. The open-weight trajectory suggests future local deployment is possible.

---

## Limitations

- Requires frozen 3D vision models for the global consistency reward — adds a preprocessing dependency
- Evaluated on three benchmarks; real-world 3D scene understanding may involve more diverse viewpoint distributions
- Map construction quality depends on view overlap; sparse or non-overlapping views degrade the global map

---

## Source

- **Paper**: [arXiv:2606.23557](https://arxiv.org/abs/2606.23557)
- **Preprint date**: Jun 2026
