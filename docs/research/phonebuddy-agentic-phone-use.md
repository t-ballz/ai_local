# PhoneBuddy: Training Open Models for Agentic Phone Use

> Source: [arXiv:2606.23049](https://arxiv.org/abs/2606.23049) · Jun 2026  
> Authors: Zhengyang Tang, Xin Lai, Pengyuan Lyu, Xinyuan Wang, Tianyi Bai, Chenxin Li, Yiduo Guo, Huawen Shen, et al.

## TL;DR

PhoneBuddy trains open-weight models (Qwen3.5-4B) for agentic phone use by combining real device environments with a lightweight mock environment called PhoneWorld, then applying SFT followed by reinforcement learning. Task success improves from 36.67% (SFT only) to 45.33% with mixed real+mock RL training.

---

## The problem

Closed-source phone agents (e.g. Apple Intelligence) are opaque and non-customizable. Open-weight alternatives face two challenges: (1) training data from real devices is expensive and slow to collect, and (2) RL on live apps is fragile — app state is non-deterministic, crashes are common, and resets are slow.

---

## How it works

**PhoneWorld**: A mock phone environment that simulates app interactions without requiring a real device. Faster episode resets and more reproducible state enable RL at scale.

**Training pipeline**:
1. **Supervised fine-tuning**: Train Qwen3.5-4B on demonstration trajectories from real device sessions
2. **Real-app RL**: RL in the actual Android environment, using task success as the reward signal
3. **Mixed RL**: Combines real-device and PhoneWorld rollouts — mock data complements real data rather than replacing it

**Key finding**: Mock-app training alone underperforms real-device RL, but mixed training achieves the best results — PhoneWorld provides coverage and speed while real-device rollouts preserve fidelity.

---

## Results

| Training regime | Task success rate |
|---|---|
| Supervised fine-tuning only | 36.67% |
| Real-app RL | 40.67% |
| Mixed RL (real + mock) | **45.33%** |

Cross-app workflows remain the hardest category.

---

## Why it matters for local AI

PhoneBuddy demonstrates that a 4B parameter model can be made competitive for phone automation tasks — small enough to run on-device on modern smartphones. The PhoneWorld mock environment pattern is reusable for other GUI automation domains (desktop, browser) where real-environment RL is too slow.

---

## Limitations

- 45.33% success is a meaningful gain but still leaves ~55% failure rate — not yet production-reliable
- Cross-app workflows (spanning multiple apps) remain unsolved
- PhoneWorld fidelity gap to real apps may limit generalization for unusual UI patterns

---

## Source

- **Paper**: [arXiv:2606.23049](https://arxiv.org/abs/2606.23049)
- **Preprint date**: Jun 2026
