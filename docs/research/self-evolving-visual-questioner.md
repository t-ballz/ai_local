# Self-Evolving Visual Questioner

> Source: [arXiv:2606.13929](https://arxiv.org/abs/2606.13929) · June 2026  
> Authors: Yijun Liang, Hengguang Zhou, Ming Li, Lichen Li, Cho-Jui Hsieh, Tianyi Zhou

## TL;DR

A VLM can bootstrap better visual question generation without any external supervision — by using itself as both proposer and filter. The self-evolving loop produces harder, more visually grounded, and more diverse questions than human-curated sets, and retraining on them improves the model's visual reasoning. Framework is backbone-agnostic and works across multiple VLM families.

---

## The problem

Training VLMs to ask good visual questions requires high-quality visual QA data — which is expensive to curate at scale. And static human-curated datasets don't keep pace with model capability: once a model has learned from a dataset, the questions become too easy.

Self-Evolving Visual Questioner breaks this dependency: the model generates its own training data, filtered for quality, in a continuous improvement loop.

---

## The self-evolution loop

```
┌─────────────────────────────────────────┐
│  1. PROPOSE: VLM generates candidate   │
│     questions for given visual inputs  │
│                      ↓                 │
│  2. REWRITE: VLM rewrites for harder  │
│     difficulty and visual grounding   │
│                      ↓                 │
│  3. FILTER: VLM evaluates and keeps   │
│     questions meeting quality bar      │
│                      ↓                 │
│  4. RETRAIN: Model trains on accepted  │
│     questions in both roles:           │
│     - as questioner (generate Q)       │
│     - as answerer (answer Q)           │
└─────────────────────────────────────────┘
           ↑ loop ────────────────────────┘
```

The VLM acts as its own teacher, critic, and student. No human labels needed after initialization.

---

## Quality dimensions evaluated

The paper introduces an assessment protocol measuring generated questions on three axes:

| Dimension | What it measures |
|-----------|-----------------|
| **Perception** | Does the question require looking at the image (not answerable from text alone)? |
| **Reasoning** | Does answering require non-trivial inference? |
| **Diversity** | Does the question set cover different aspects of the image? |

---

## Key results

- Self-evolved questions outperform human-curated baselines on all three dimensions
- Retraining on self-evolved data improves VLM performance on downstream visual reasoning benchmarks
- Framework tested across multiple backbone VLMs — improvements consistent across architectures

---

## Why it matters

Self-improvement loops for VLMs are an active area (analogous to RLVR for text LLMs, but without a verifiable reward signal). This work shows that **question quality** is a viable self-improvement axis — the model can teach itself to see more carefully by asking better questions.

---

## Source

- **Paper**: [arXiv:2606.13929](https://arxiv.org/abs/2606.13929)
