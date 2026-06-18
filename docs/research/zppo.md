# ZPPO: Zone of Proximal Policy Optimization

> Source: [arXiv:2606.18216](https://arxiv.org/abs/2606.18216) · June 2026  
> Authors: Byung-Kwan Lee, Ximing Lu, Shizhe Diao, et al. (NVIDIA, UW, NTU)

## TL;DR

ZPPO distills a large teacher model into a small student by embedding teacher guidance **in prompts**, not gradients. Two prompt strategies (BCQ and NCQ) keep the student in its "zone of proximal development" — hard enough to learn, not so hard it collapses. Tested on Qwen3.5 at 0.8B–9B with a 27B teacher, ZPPO beats off-policy distillation, on-policy distillation, and GRPO across 31 benchmarks. Strongest gains are at the smallest model scale.

---

## The problem with standard distillation

**Off-policy distillation**: student imitates teacher rollouts, but the teacher's outputs may be far outside the student's current ability — the student can't learn from trajectories it can't reach.

**On-policy distillation with gradient injection**: injecting teacher responses on failed rollouts causes policy drift — the gradient signal contradicts the student's own exploration.

ZPPO avoids both by keeping the student's RL objective intact and delivering teacher guidance purely as *reformulated prompts*.

---

## How ZPPO works

### BCQ: Binary Candidate-included Question

The student is shown both:
- One **correct** teacher response (anonymized)
- One **incorrect** student response (anonymized)

It must discriminate between them without knowing which is which. This scaffolds learning without telling the student the answer directly.

### NCQ: Negative Candidate-included Question

The student's own **failed rollouts** are aggregated into a single prompt. The student must identify the shared failure pattern across its mistakes — a self-diagnostic signal that doesn't require a teacher at inference time.

### Replay buffer

Hard questions circulate in a buffer and are re-exposed via BCQ/NCQ until the student achieves ≥50% mean accuracy ("graduates") or the question is evicted FIFO under capacity constraints. This targets training effort at the student's current frontier — hence "zone of proximal development."

---

## Results

Models: **Qwen3.5** at 0.8B, 2.4B, 7B, 9B | Teacher: **27B** model | Evaluation: 31-benchmark suite

| Baseline | ZPPO beats? |
|----------|-------------|
| Off-policy distillation | ✓ |
| On-policy distillation | ✓ |
| GRPO (RL without teacher) | ✓ |

Improvements are **largest at the smallest scale** (0.8B) — the zone where distillation failure modes are most severe.

---

## Why it matters

- Works with any open-weight teacher + student pair via standard RL infrastructure
- No changes to the student's underlying policy gradient objective
- Particularly useful for compressing 27B+ reasoning models into sub-10B deployable models
- The BCQ/NCQ prompts are simple to implement — no new training infrastructure required

---

## Source

- **Paper**: [arXiv:2606.18216](https://arxiv.org/abs/2606.18216)
