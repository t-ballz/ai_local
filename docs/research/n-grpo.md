# N-GRPO: Semantic Neighbor Mixing for GRPO

> Source: [arXiv:2606.10768](https://arxiv.org/abs/2606.10768) · June 2026

## TL;DR

GRPO needs diverse rollouts, but the two common approaches both fail: token-level sampling (high temperature) produces incoherent trajectories; embedding-level random noise disrupts semantic consistency. N-GRPO fixes this with **Semantic Neighbor Mixing** — constructing input representations by interpolating an anchor token's embedding with its nearest semantic neighbors. Diversity is injected while staying strictly on the local semantic manifold. Consistent improvements on math reasoning benchmarks across DeepSeek-R1-Distill-Qwen model sizes.

---

## The GRPO diversity problem

Group Relative Policy Optimisation trains by generating multiple rollouts per problem, scoring them, and updating toward better ones. Diversity in rollouts is critical — identical attempts provide no learning signal.

| Approach | Diversity type | Problem |
|----------|---------------|---------|
| High-temperature sampling | Token-level noise | Incoherent trajectories; semantically broken paths |
| Embedding-level random noise | Continuous perturbation | Disrupts semantic coherence; off-manifold representations |
| **N-GRPO (Semantic Neighbor Mixing)** | **Manifold-constrained** | None — diversity stays semantically valid |

---

## How Semantic Neighbor Mixing works

For each input token embedding, N-GRPO:

1. Finds the token's **nearest semantic neighbors** in embedding space
2. **Mixes** the anchor embedding with one or more neighbors (weighted interpolation)
3. The resulting representation is a point on the local semantic manifold — a meaningful direction, not random noise

The mixed embeddings are used as rollout inputs. Different mixing weights → different but coherent reasoning trajectories → genuine policy-level diversity.

The key property: unlike random noise, neighbor mixing can only produce combinations that exist on or near the learned semantic manifold, so rollouts stay logically structured.

---

## Relation to S2L-PO

Both N-GRPO and [S2L-PO](s2l-po-grpo-diversity.md) attack the same GRPO diversity problem:

| | S2L-PO | N-GRPO |
|--|--------|--------|
| Diversity source | Frozen smaller model from same family | Semantic neighbor mixing in embedding space |
| Requires extra model? | Yes (sibling model) | No |
| Diversity level | Policy-level (whole trajectory) | Input-level (per token, manifold-constrained) |

N-GRPO has a lower infrastructure cost (no second model needed), while S2L-PO provides coarser but potentially more structural diversity.

---

## Results

Evaluated on DeepSeek-R1-Distill-Qwen models across multiple sizes:

- Consistent improvements on math reasoning benchmarks over strong GRPO baselines
- Robust generalisation across model sizes
- No additional inference-time cost vs standard GRPO

---

## Source

- **Paper**: [arXiv:2606.10768](https://arxiv.org/abs/2606.10768)
