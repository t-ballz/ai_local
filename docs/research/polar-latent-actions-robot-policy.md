# PoLAR: Factorizing Extent and Mode in Latent Actions

> Source: [arXiv:2606.21139](https://arxiv.org/abs/2606.21139) · Jun 2026  
> Authors: Youngjoon Jeong, Jihwan Yu, Minsoo Jo, Junha Chun, Taesup Kim

## TL;DR

PoLAR structures the latent action space for robot policy pretraining by imposing radial geometry: radius encodes *how much* change occurs (transition extent), direction encodes *what kind* of change (transition mode). Using hyperbolic space and temporal gaps as extent proxies, PoLAR improves downstream policy performance over existing latent action and vision-language pretrained baselines.

---

## The problem

Pretraining robot policies from video requires learning latent action representations — compressed encodings of what happened between frames. Existing approaches treat the latent action space as an unstructured embedding space, offering no inductive bias about the geometry of actions.

The key insight this work exploits: not all actions are equal. Small adjustments (tweaking a grasp) and large movements (reaching across a workspace) are qualitatively different, and this difference in *extent* should be reflected in the representation — not mixed arbitrarily with the *type* of action.

---

## How it works

**Radial factorization**: PoLAR imposes a radial structure on the latent space:
- **Radius** → transition extent (how much the world changed)
- **Direction** → transition mode (what kind of change occurred)

**Temporal gaps as extent proxy**: During pretraining, the temporal distance between two observations is used as a proxy for the magnitude of state change between them. Large temporal gaps → large extent → large radius. This provides a self-supervised training signal without requiring explicit action labels.

**Hyperbolic geometry**: The latent space uses hyperbolic (rather than Euclidean) geometry, because hyperbolic volume expands with radius — providing more representational capacity for diverse transition modes at larger extents, which matches the empirical distribution of robot actions (small adjustments are common, large diverse movements are rarer but require richer encoding).

---

## Results

Evaluated across simulation and real-world robotic manipulation tasks. PoLAR improves downstream policy performance over:
- Existing latent action pretraining approaches
- Strong pretrained vision-language model baselines

---

## Why it matters for local AI

Robot policy pretraining from video is a tractable local workload — it doesn't require real-time robotic hardware, just video datasets. PoLAR's geometric insight (radius = extent, direction = mode) is a clean structural prior that improves data efficiency for policy learning. The hyperbolic geometry choice is also applicable to other action-conditioned representation learning problems.

---

## Limitations

- Hyperbolic geometry adds implementation complexity vs. standard Euclidean embeddings
- Temporal gap as extent proxy assumes consistent frame rate and action pacing in training video — violations may produce noisy extent signals
- Real-world experiments are on manipulation tasks; locomotion or navigation may have different extent/mode distributions

---

## Source

- **Paper**: [arXiv:2606.21139](https://arxiv.org/abs/2606.21139)
- **Preprint date**: Jun 2026
