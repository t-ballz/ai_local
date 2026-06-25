# Connect the Dots: RL for Long-Lifecycle Cross-Domain Agents

> Source: [arXiv:2606.20002](https://arxiv.org/abs/2606.20002) · Jun 2026  
> Authors: Yanxi Chen, Weijie Shi, Yuexiang Xie, Boyi Hu, Yaliang Li, Bolin Ding, Jingren Zhou

## TL;DR

Connect the Dots trains LLMs to act as long-lifecycle agents that continuously explore environments, learn from experience, and self-update over extended RL rollouts. The framework provides end-to-end RL infrastructure for long sequences, specialized training environments, and empirical validation of both in-distribution and out-of-distribution generalization.

---

## The problem

Current LLM agents are episodic: each task starts fresh, with no carry-over from prior interactions. A long-lifecycle agent, by contrast, should:

1. **Accumulate experience** across many episodes in the same environment
2. **Self-update** — modify its own behavior based on what it learned, without human retraining
3. **Generalize across domains** — transfer learned strategies to environments it hasn't seen during training

Existing RL infrastructure for LLMs targets short rollouts; end-to-end optimization over hundreds of steps in a persistent environment is technically unsolved and computationally expensive.

---

## How it works

**End-to-end RL for long rollouts**: Extended infrastructure supporting long episode sequences — managing memory, gradient accumulation, and reward signals across hundreds of steps without the context truncation problems that arise in standard RLHF pipelines.

**Specialized training environments**: Custom environments designed to develop the *meta-capability* of long-lifecycle adaptation — problems where the optimal strategy changes over time and where past experience is genuinely useful (not just a distraction).

**Self-updating mechanism**: The agent can modify its own behavior policies during a long episode, using RL signals from its own experience rather than waiting for offline retraining.

---

## Results

Empirical validation demonstrates both in-distribution and out-of-distribution generalization — the agent transfers learned meta-strategies to environments not seen during training. Code and environments released alongside the paper.

---

## Why it matters for local AI

Long-lifecycle agents are the direction of agentic AI: a local agent that gets smarter at *your specific use cases* over time, without retraining on a dataset curated by someone else. Connect the Dots provides the RL infrastructure and training environment design to study this property. The OOD generalization result suggests the learned meta-strategy is transferable, not just environment-specific memorization.

---

## Limitations

- Work described as in progress with ongoing updates — results and methods may change
- Compute requirements for long-rollout RL are high compared to standard RLHF
- OOD generalization measured in controlled settings; real-world domain shift may be harder

---

## Source

- **Paper**: [arXiv:2606.20002](https://arxiv.org/abs/2606.20002)
- **Preprint date**: Jun 2026
