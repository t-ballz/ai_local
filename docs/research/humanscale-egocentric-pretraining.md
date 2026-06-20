# HumanScale: Egocentric Human Video Can Outperform Real-Robot Data for Embodied Pretraining

> Source: [arXiv:2606.20521](https://arxiv.org/abs/2606.20521) · June 2026  
> Authors: Ma, Juncheng; Bi, Jianxin; Deng, Yufan; et al. (MIT-IBM, etc.)

## TL;DR

Egocentric human video, when processed through careful filtering and labeling, outperforms teleoperated real-robot trajectories for embodied foundation model pretraining. A two-stage approach—pretrain on diverse human video, then adapt with small amounts of robot data for action-space alignment—achieves 24% lower validation loss and 90% higher success on out-of-distribution robot tasks.

---

## The problem

Embodied foundation models need massive amounts of training data to match the scaling benefits seen in large language models, but face a severe bottleneck: teleoperated real-robot trajectories, the current gold standard, are expensive, difficult to collect, behaviorally narrow, and environmentally limited. This scalability wall prevents the field from building truly large-scale embodied models. Egocentric human video offers a tantalizing alternative—abundant, cheap, and diverse—but its viability as a pretraining source remained unexplored.

---

## The two-stage pretraining paradigm

Rather than force egocentric video and robot data into a single training process (with all its embodiment and action-space mismatches), HumanScale uses a **two-stage approach**:

1. **Pretrain on egocentric human video** — Learn diverse world representations, visual patterns, and general manipulation concepts from massive amounts of human-collected video.
2. **Adapt with labeled robot data** — Fine-tune on a small corpus of teleoperated robot trajectories to align the learned representations with robot-specific action spaces and embodiments.

This design recognizes that the two data sources contribute different strengths: humans provide scale and behavioral diversity; robots provide precise action supervision and embodiment alignment. Both are leveraged, neither dominates.

---

## Key results

Egocentric pretraining consistently beats robot-only baselines under equal data volume:

- **24% lower validation loss** on real-robot action prediction
- **52.5% higher success rate** on in-distribution real-robot manipulation tasks
- **90% higher success rate** on out-of-distribution real-robot tasks

The out-of-distribution gains are particularly striking—they suggest that egocentric pretraining learns richer, more generalizable world models than robot-only pretraining, even though robot trajectories carry precise action labels.

---

## Why it matters

This work directly challenges the assumption that more robot data is always better. By showing that egocentric video can be a superior pretraining signal, it:

1. **Unblocks scaling** — egocentric video is orders of magnitude more abundant than robot data, removing a critical bottleneck for embodied foundation models.
2. **Reduces costs** — fewer robots and operators needed; data collection shifts toward commodity video sources.
3. **Improves generalization** — the diversity in human video translates to better out-of-distribution performance on real robots.
4. **Validates a scalable paradigm** — pretraining on internet-scale data, adapting to task-specific embodiments with modest labeled data. This mirrors the successful playbook from language models (pretrain large, finetune focused).

---

## Source

- **Paper**: [arXiv:2606.20521](https://arxiv.org/abs/2606.20521)
