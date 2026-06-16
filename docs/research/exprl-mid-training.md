# ExpRL: Exploratory RL for LLM Mid-Training

> Source: [arXiv:2606.17024](https://arxiv.org/abs/2606.17024) · Violet Xiang, Amrith Setlur, Chase Blagden, Nick Haber, Aviral Kumar · June 2026

## TL;DR

Standard mid-training uses SFT on curated reasoning traces to prime models before final RL. ExpRL replaces that SFT with RL itself — but dense RL, where an LLM judge scores both intermediate steps and final answers against a reference solution used as a grading rubric rather than an imitation target. On challenging math reasoning, ExpRL provides a better RL initialisation than SFT, sparse GRPO, and self-distillation.

---

## What is mid-training?

LLM training has three phases:

| Phase | What happens |
|-------|-------------|
| **Pre-training** | Next-token prediction on massive text; builds broad knowledge |
| **Mid-training** | Curated reasoning traces teach structured problem-solving skills |
| **Final RL** | Sparse-reward RL (e.g. GRPO) refines reasoning toward correct answers |

Mid-training is the "priming" phase — it sets up the model for final RL to work efficiently. Currently, mid-training is done with SFT on high-quality reasoning demonstrations. ExpRL asks: what if we used RL here instead?

---

## The problem with sparse rewards in mid-training

Sparse rewards (correct/incorrect final answer) work in final RL because the model is already good enough to produce correct answers occasionally — the signal is noisy but present.

In mid-training, the model is still learning basic reasoning primitives. Sparse rewards fail to upweight:
- Useful intermediate reductions (progress toward a solution)
- Correct reasoning strategies that reach wrong answers due to arithmetic errors
- Productive exploration behaviours that don't immediately pay off

SFT sidesteps this by simply imitating traces, but imitation can't teach the model to explore or recover from mistakes.

---

## ExpRL: reference solutions as reward scaffolds

The key reframe: treat reference solutions not as **imitation targets** (SFT) but as **reward scaffolds**.

In ExpRL:
1. Reference solutions are **hidden from the policy** — the model never sees them as demonstrations
2. They are used only to build **problem-specific grading rubrics** for an LLM judge
3. The LLM judge scores the model's on-policy reasoning traces against these rubrics

Two reward levels:
- **Outcome-level**: did the final answer match?
- **Process-level**: did intermediate steps show useful progress, valid reductions, sound reasoning?

The dense signal lets the model learn from partial progress and intermediate structure, not just from fully correct solutions.

---

## Results

Evaluated on challenging math reasoning tasks:

| Method | RL priming quality |
|--------|-------------------|
| SFT on demonstrations | Baseline |
| Sparse-reward GRPO | Worse than SFT |
| Self-distillation | Worse than SFT |
| **ExpRL (dense LLM-judge rewards)** | **Best** |

ExpRL also provides a better initialisation for **subsequent sparse-reward RL** — the final RL phase converges faster and to higher performance when started from an ExpRL-primed checkpoint rather than an SFT checkpoint.

---

## Relation to other work

| Method | Where it sits | Reward signal |
|--------|--------------|---------------|
| SFT (standard mid-training) | Mid-training | None — supervised imitation |
| GRPO | Final RL | Sparse (binary correct/incorrect) |
| [S2L-PO](s2l-po-grpo-diversity.md) | Final RL | Sparse, but diverse rollouts via small model |
| [N-GRPO](n-grpo.md) | Final RL | Sparse, but diverse rollouts via embedding mixing |
| **ExpRL** | **Mid-training** | **Dense, process + outcome, LLM judge** |

ExpRL is complementary to S2L-PO and N-GRPO: those improve rollout diversity during final RL; ExpRL improves the initialisation that final RL starts from.

---

## Source

- **Paper**: [arXiv:2606.17024](https://arxiv.org/abs/2606.17024)
