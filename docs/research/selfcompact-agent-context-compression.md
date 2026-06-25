# SelfCompact: Autonomous Context Compression for LLM Agents

> Source: [arXiv:2606.23525](https://arxiv.org/abs/2606.23525) · Jun 2026  
> Authors: Tianjian Li, Jingyu Zhang, William Jurayj, Xi Wang, Chuanyang Jin, Mehrdad Farajtabar, Eric Nalisnick, Daniel Khashabi

## TL;DR

SelfCompact lets LLM agents decide *when* to compress their own context rather than compacting on a fixed schedule. A lightweight decision policy activates summarization when subtasks complete or progress stalls, and suppresses it during active reasoning. Across six benchmarks and seven models, it matches or beats fixed-interval summarization with 30–70% lower token cost — up to +18.1 points on math tasks.

---

## The problem

Long agent interactions accumulate outdated, redundant information that wastes context budget and eventually causes context overflow. Fixed-schedule compaction (every N turns, or at a hard context limit) is either too aggressive — compressing mid-reasoning and losing critical intermediate state — or too conservative — letting stale history pile up. Models themselves often can't recognize when their context has degraded; they need scaffolding to manage it.

---

## How it works

**Compaction tool**: A summarization function the model can call to collapse old context into a compact summary. The summary is appended; the replaced history is discarded.

**Decision framework**: A lightweight policy defines two conditions:

| Condition | Action |
|---|---|
| Subtask boundary reached | Compact — old task state no longer needed |
| Progress has plateaued | Compact — stuck context unlikely to help |
| Active derivation in progress | Suppress — mid-reasoning compaction loses intermediate state |
| Model is stuck (repeated failures) | Suppress — compaction won't fix the underlying issue |

No additional training is required — the decision policy is rule-based scaffolding that wraps the existing model.

---

## Results

| Benchmark type | Gain over fixed-interval |
|---|---|
| Mathematical tasks | Up to +18.1 points |
| Search-based tasks | +5–9 points |
| Token cost reduction | 30–70% across 6 benchmarks × 7 models |

Performance is comparable or better than fixed-interval summarization across all tested configurations.

---

## Why it matters for local AI

Context management is a practical bottleneck for local agents with finite VRAM. SelfCompact's decision-aware approach avoids the failure mode of compacting at the wrong moment — which can corrupt agent state mid-task. The 30–70% token savings translate directly to faster inference and lower memory pressure on consumer hardware. No fine-tuning required.

---

## Limitations

- Decision policy is rule-based; edge cases (ambiguous subtask boundaries, complex multi-branch reasoning) may trigger at wrong moments
- Summarization quality depends on the base model — a weak model may produce lossy summaries
- Evaluated on six benchmarks; very long (>100K token) real-world agent sessions not tested

---

## Source

- **Paper**: [arXiv:2606.23525](https://arxiv.org/abs/2606.23525)
- **Preprint date**: Jun 2026
