# OPD-Evolver: Self-Evolving Agents via On-Policy Distillation

> Source: [arXiv:2606.17628](https://arxiv.org/abs/2606.17628) · June 2026  
> Authors: Guibin Zhang, Xun Xu, Yanwei Yue, Zikun Su, Wangchunshu Zhou, Xiaobin Hu, Shuicheng Yan

## TL;DR

OPD-Evolver teaches agents not just to *use* memory but to *evolve through it*. A dual-loop architecture separates fast test-time evolution (using a 4-level memory hierarchy) from slow offline distillation (distilling high-value experience back into the policy weights). A 9B OPD-Evolver model competes with Qwen3.5-397B-A17B and Step-3.5-Flash on agent benchmarks, beating memory-augmented baselines by up to **11.5%**.

---

## The gap in memory-augmented agents

Existing self-evolving agents accumulate experience in memory but don't actually *learn* from it — they retrieve and apply past episodes without updating their core reasoning capabilities. Memory becomes a lookup table, not a learning signal.

OPD-Evolver closes this gap: the agent's experience is distilled into the policy itself, making future episodes cheaper and more reliable even without memory retrieval.

---

## Architecture: dual-loop co-evolution

### Fast loop (test-time evolution)

The agent interacts with a **4-level memory hierarchy**:

| Level | Role |
|-------|------|
| **Read** | Retrieve relevant past experience |
| **Use** | Apply retrieved experience to current task |
| **Write** | Record new outcomes and observations |
| **Maintain** | Curate and prune memory for long-term utility |

These four operations run at inference time, enabling rapid adaptation across a session.

### Slow loop (offline distillation)

After episodes accumulate:

1. **Outcome-calibrated attribution**: which memory operations actually contributed to good outcomes?
2. **Privileged hindsight**: look at what actually happened to re-label which operations were valuable
3. **On-policy self-distillation**: distill the four memory capabilities (read/use/write/maintain) back into the base policy

The policy learns to internalize the best memory behaviors — reducing dependence on explicit retrieval over time.

---

## Results

| Baseline | OPD-Evolver 9B gain |
|----------|---------------------|
| ReasoningBank | +11.5% |
| Skill0 (training-based) | +5.8% |

**The 9B OPD-Evolver competes with Qwen3.5-397B-A17B and Step-3.5-Flash** — models ~40× larger — on agent benchmarks.

---

## Why it matters

- Demonstrates that agent capability can be compressed into smaller models via experience distillation
- The 4-level memory hierarchy provides a structured framework for agent memory systems (not just "store everything")
- On-policy self-distillation without requiring a separate teacher model

---

## Source

- **Paper**: [arXiv:2606.17628](https://arxiv.org/abs/2606.17628)
