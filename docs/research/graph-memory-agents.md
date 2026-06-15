# Memory is Reconstructed, Not Retrieved

> Source: [arXiv:2606.06036](https://arxiv.org/abs/2606.06036) · [github.com/Ji-shuo/MRAgent](https://github.com/Ji-shuo/MRAgent) · June 5, 2026

## TL;DR

Standard agent memory retrieves a fixed snapshot and hands it to the model. MRAgent instead treats memory as something the agent **actively reconstructs** — iterating through a heterogeneous graph, following associative links, pruning dead ends — the same way human memory actually works. On LoCoMo it scores 84.21 vs the next best 68.31 (+23.3%), while using 5× fewer tokens than A-Mem.

---

## The problem with retrieve-then-reason

Most memory-augmented agents: embed a query → find top-k chunks → stuff them into the prompt → reason. The retrieval step is blind to what the model discovers mid-reasoning. If step 2 of the model's chain of thought reveals a new entity worth retrieving, there's no path back to memory.

The result: single-hop recall is fine, multi-hop compositional queries fail because the retrieval budget is spent before the model knows what it actually needs.

---

## MRAgent: active reconstruction

Two components:

### 1. Cue–Tag–Content memory graph

Memory is stored as a three-layer heterogeneous graph:

| Layer | What it holds |
|-------|--------------|
| **Episodic** | Concrete events with timestamps (conversations, observations) |
| **Semantic** | Stable facts: preferences, attributes, recurring patterns |
| **Abstraction** | High-level topic summaries across recurring themes |

Nodes in adjacent layers are linked by **associative tags** — semantic bridges that let traversal jump from a specific cue to related content without scanning everything.

### 2. Active reconstruction traversal

At query time, the agent doesn't retrieve once. It traverses the graph iteratively:

```
LLM reasons over current state
        ↓
Forward: Cue → Tag → Content
  or Reverse: Content → Tag → Cue
        ↓
Prune branches that don't match evidence
        ↓
Stop when sufficient evidence accumulated
```

**Theorem 4.1** (proved in the paper): active retrieval policies are strictly more expressive than passive ones. On a binary-tree needle-in-haystack problem, active retrieval achieves zero error in polynomial budget; passive retrieval needs exponential budget.

---

## Results

| Benchmark | MRAgent | Best baseline | Gain |
|-----------|---------|--------------|------|
| LoCoMo (Gemini backbone) | **84.21** | 68.31 | +23.3% |
| LoCoMo (Claude backbone) | — | — | +12.4% |
| LongMemEval | — | — | +32% |

**Token efficiency**: 118K prompt tokens vs A-Mem's 632K — active pruning means the model never sees irrelevant branches.

**Multi-turn behaviour**: Single-hop queries resolve in ~3 turns. Multi-hop queries improve +30%+ across successive steps; the agent self-terminates when it has enough evidence.

---

## What this means for agent design

1. **Memory ≠ a retrieval index.** The most powerful memory design lets reasoning inform retrieval and vice versa in a loop, not a pipeline.
2. **Associative tags are the key structural primitive.** They replace exhaustive graph expansion with semantic routing — the difference between a search and a guided walk.
3. **Defer relational reasoning to query time.** Build memory fast; resolve relationships only when queried. This keeps construction cheap and retrieval rich.
4. **The token cost trade-off**: fewer tokens per query, but latency grows with reconstruction depth (acknowledged limitation).

---

## Source

- **Paper**: [arXiv:2606.06036](https://arxiv.org/abs/2606.06036)
- **Code**: [github.com/Ji-shuo/MRAgent](https://github.com/Ji-shuo/MRAgent)
