# ActWorld: Interactive World Models with Action-Aware Memory

> Source: [arXiv:2606.17730](https://arxiv.org/abs/2606.17730) · June 2026  
> Authors: Zhexiao Xiong, Yizhi Song, Hao Kang, Qing Yan, Liming Jiang, et al.

## TL;DR

World models can navigate — but they can't manipulate objects. ActWorld fixes this with a **hierarchical action-aware memory** that routes history compression by interaction significance rather than recency. Combined with a 100K interaction video dataset, it enables a single model to support both flexible navigation and sophisticated object manipulation — 2× the success rate of navigation-only baselines on complex interaction tasks.

---

## The navigation gap

Current interactive world models are built around *navigation*: move forward, turn, pan camera. They accumulate visual history and use recency-biased compression (discard old frames, keep recent ones) — which works for navigation because context is spatially continuous.

Object manipulation breaks this assumption. When you pick up, move, or interact with an object, the **transition frame** is critical even if it was 50 steps ago. Recency-biased compression discards exactly the frames that matter.

ActWorld calls this **action-forgetting pathology**.

---

## Two solutions

### 1. Hierarchical Action-Aware Memory

Instead of discarding frames by age, memory routes compression based on **interaction significance**:

- Frames containing object interactions are flagged and retained regardless of recency
- Navigational frames are still compressible
- The compression budget is allocated according to what the model actually did, not when

Two components:

**Event-Aware Frame Re-Assignment (EAFR)**: Identifies interaction events and reclassifies frames into retained/compressible based on whether they contain significant manipulation events.

**Persistent Memory Bank**: Maintains **event-update tokens** (what changed) and **object-identity tokens** (what is that object) throughout extended simulations. These persist across the full rollout, not just a recency window.

### 2. Interaction Video Dataset

Existing world model training data focuses on navigation. ActWorld contributes:
- **100K interaction videos** — human-object manipulation captured from egocentric view
- Each video annotated with **per-chunk captions via chain-of-thought reasoning**, providing rich textual grounding for what interactions are happening

---

## Results

ActWorld substantially outperforms navigation-only baselines on complex interaction tasks while maintaining comparable viewpoint control quality. A single unified model replaces the previously separate navigation and manipulation systems.

---

## Why it matters

World models are a promising substrate for embodied agents and game AI. ActWorld establishes that **memory architecture**, not just model scale, is a key bottleneck for extending world models from passive exploration to active interaction — a prerequisite for any agent that must manipulate its environment.

---

## Source

- **Paper**: [arXiv:2606.17730](https://arxiv.org/abs/2606.17730)
