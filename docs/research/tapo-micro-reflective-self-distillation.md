# TAPO: Micro-Reflective Trajectories for Self-Distillation

> Source: [arXiv:2606.18844](https://arxiv.org/abs/2606.18844) · Jun 2026  
> Authors: Zhilin Huang, Hang Gao, Ziqiang Dong, Yuan Chen, Yifeng Luo, Chujun Qin, Jingyi Wang, Yang Yang, Guanjun Jiang

## TL;DR

TAPO (Trajectory-Augmented Policy Optimization) builds training trajectories that retain the model's erroneous reasoning up to the point of failure, then insert a natural-language diagnosis — teaching the model to self-correct from its own mistakes rather than just imitating correct solutions. Consistent gains on AIME 2024/2025 and HMMT 2025.

---

## The problem

Standard self-distillation for LLMs uses correct rollouts as training signal. The model learns to imitate good outputs but never learns *why* its reasoning failed or how to recover from errors mid-chain. Implicit alignment methods (DPO, RLHF) don't surface the error location explicitly, making it hard for the model to learn targeted correction behavior.

---

## How it works

**Micro-reflective trajectory construction**: For each problem, TAPO collects both a correct and an incorrect model rollout. It identifies the first divergence point in the incorrect chain — the step where the reasoning goes wrong — and inserts a natural-language diagnosis at that exact location. The resulting trajectory looks like:

```
[correct reasoning... ] → [wrong step] → [DIAGNOSIS: "Error: confused X with Y"] → [corrected continuation...]
```

**Contrastive pairs**: These augmented trajectories are paired with unaugmented correct rollouts to form contrastive training data. The model learns to distinguish error-recovery behavior from normal reasoning.

**Policy optimization**: Training uses standard policy optimization over these augmented trajectories, requiring no extra model or training infrastructure beyond what's needed for basic SFT.

---

## Results

Tested on math competition benchmarks: AIME 2024, AIME 2025, HMMT 2025. TAPO shows consistent gains over existing self-distillation approaches on both initial reasoning quality and error-correction capability.

---

## Why it matters for local AI

Self-distillation without external supervision is the key scaling path for local models — you can't rely on GPT-4 labels indefinitely. TAPO's micro-reflection approach provides a mechanism for models to improve from failure, not just success, using their own generated data. The approach is model-agnostic and adds no inference infrastructure.

---

## Limitations

- Evaluated primarily on mathematical reasoning; applicability to open-ended or coding tasks requires further study
- Diagnosis insertion quality depends on the model's ability to correctly identify the failure point — errors in diagnosis may produce noisy training signal
- Requires paired correct/incorrect rollouts, which may be expensive to collect for hard problems

---

## Source

- **Paper**: [arXiv:2606.18844](https://arxiv.org/abs/2606.18844)
- **Preprint date**: Jun 2026
