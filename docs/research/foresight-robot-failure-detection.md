# Foresight: Failure Detection for Long-Horizon Robot Manipulation

> Source: [arXiv:2606.23085](https://arxiv.org/abs/2606.23085) · Jun 2026  
> Authors: Haoran Zhang, Yifu Lu, Boyang Wang, Xuhui Kang, Yen-Ling Kuo, Zezhou Cheng, Mengdi Wang, Odest Chadwicke Jenkins

## TL;DR

Foresight detects when long-horizon robotic manipulation tasks are failing by monitoring latent representations from an action-conditioned world model, using only binary success/failure labels for training (no temporal annotations). Functional conformal prediction auto-calibrates thresholds, and the approach works across different control policies in both simulation and physical robots.

---

## The problem

Long-horizon manipulation tasks — multi-step sequences like "pick up the cup, put it in the dishwasher, close the door" — can fail silently. A robot may take a wrong action mid-sequence that doesn't immediately produce an observable error but dooms the task. Detecting these failures early requires monitoring that:

1. Doesn't need dense per-timestep supervision (expensive to label)
2. Works across different control policies (not policy-specific)
3. Adapts its detection threshold to the specific task without manual tuning

---

## How it works

**Action-conditioned world model latents**: The monitor uses a pre-trained world model that takes the current observation and action as input and predicts the next state. The latent representation of this prediction captures the expected trajectory of the task.

**Binary-label training**: Rather than requiring timestep-level annotations, the monitor is trained only on whether the full episode succeeded or failed — labels that are easy to collect from real trials.

**Functional conformal prediction**: An adaptive thresholding method from conformal prediction theory that automatically calibrates the failure detection threshold from a small set of calibration trials, without manual tuning per policy or task.

---

## Results

Evaluated in simulation and on physical robots across multiple control policies. Action-conditioned world model embeddings provide reliable failure detection across policy variants — the representation transfers across control strategies.

---

## Why it matters for local AI

Failure detection is the missing link for autonomous local robot deployments. Without it, a robot that gets stuck mid-task continues executing futile actions until a human intervenes. Foresight's binary-label training is practically important: collecting "did the task succeed?" labels is cheap; collecting timestep annotations is not. The conformal prediction calibration avoids per-deployment manual tuning.

---

## Limitations

- Relies on an action-conditioned world model being available — not every robot control stack has one
- Binary labels mean the monitor can detect failure but not diagnose its cause
- Evaluated on manipulation tasks; applicability to locomotion or navigation is unverified

---

## Source

- **Paper**: [arXiv:2606.23085](https://arxiv.org/abs/2606.23085)
- **Preprint date**: Jun 2026
