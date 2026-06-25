# WorldLines: Benchmarking Long-Horizon Stateful Embodied Agents

> Source: [arXiv:2606.18847](https://arxiv.org/abs/2606.18847) · Jun 2026  
> Authors: Yehang Zhang, Jianchong Su, Haojian Huang, Yifan Chang, Tianhao Zhou, Xinli Xu, Yingjie Xu, Yinchuan Li, Zexi Li, Ying-Cong Chen

## TL;DR

WorldLines is a benchmark for embodied agents that must maintain persistent state across long household task sequences, paired with ObsMem — a reference architecture that separates visibility-aware memories from action-native state trails. Experiments reveal that current memory systems fail systematically under state mutations and partial observability.

---

## The problem

Most embodied AI benchmarks test short-horizon tasks where the agent only needs to track state for a few steps. Real household tasks unfold over minutes: objects move, devices change state, prior actions have consequences. Existing approaches fall into two camps that each miss something:

- **Language-based retrieval**: Handles long history but doesn't track world state changes
- **Short-horizon execution**: Tracks state but forgets older context

No standard benchmark existed that forced agents to maintain accurate world models across extended, stateful interactions.

---

## How it works

**WorldLines Benchmark**: Generates temporally extended household traces including dialogues, actions, execution feedback, and object/device state changes. Converts these into two evaluation modes:

1. **Memory QA**: Question answering grounded in evidence from the trace (e.g. "What state is the dishwasher in now?")
2. **Embodied Task Planning**: Requires executing real-world actions based on accumulated state knowledge

**ObsMem Framework**: A reference architecture designed for this setting. Two core components:

- **Visibility-aware memories**: Tracks only what the agent can actually observe in partial observability settings — avoids hallucinating state for unobserved objects
- **Action-native state trails**: Records world state changes caused directly by agent actions, maintaining a causal record that's easier to query than raw transcript history

The combination provides stronger baselines for both evaluation modes than retrieval-only or execution-only approaches.

---

## Results

Experiments identified three persistent failure modes in current systems:

| Failure mode | Description |
|---|---|
| Partial observability | Agents hallucinate state for objects not yet seen |
| Overwritten states | Agents fail to update beliefs when object state changes |
| Memory-to-plan gap | Long-term memories don't translate into correct executable plans |

ObsMem provides measurable improvements on both Memory QA and Embodied Task Planning vs. baseline memory approaches, with the largest gains on state-mutation scenarios.

---

## Why it matters for local AI

The ObsMem architecture pattern is directly applicable to any local agent system where state tracking matters:

- **Visibility-aware memory** prevents hallucination in perception-limited settings (robot cameras, partial DOM states in browser agents)
- **Action-native state trails** are a simpler alternative to full world-model simulation — record what *changes*, not everything
- The benchmark provides a reproducible way to compare memory architectures across agent frameworks

---

## Limitations

- Household domain only; generalization to other settings (coding agents, web agents) requires new benchmark construction
- ObsMem is a reference architecture, not a deployable system — implementation details depend on the agent framework
- Evaluation tasks are synthetic; gap to real household deployment is unknown

---

## Source

- **Paper**: [arXiv:2606.18847](https://arxiv.org/abs/2606.18847)
- **Preprint date**: Jun 2026
