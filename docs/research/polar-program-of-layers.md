# PoLar: Program-of-Layers for LLM Inference

> Source: [arXiv:2606.06574](https://arxiv.org/abs/2606.06574) · ICML 2026

## TL;DR

Every LLM inference run executes exactly the same sequence of layers for every token, regardless of how hard the problem is. **PoLar** breaks this constraint: a tiny 2.1M-parameter predictor decides, per input, which layer segments to skip and which to repeat. Result: **+3.8–5.8% accuracy on DART-Math**, often with *less* compute than the fixed baseline.

---

## The insight

Fixed-depth execution is a narrow constraint on LLM capacity. A model trained with a fixed 32-layer forward pass has learned computations distributed across those layers — but not every input needs every layer at the same depth. Some inputs might benefit from running certain layers twice; others might skip a layer entirely without loss.

The paper proves this empirically: Monte Carlo Tree Search over layer execution programs finds better programs than the fixed sequence for the majority of test inputs.

---

## How PoLar works

### 1. Program representation

The layer stack is divided into **contiguous segments** (up to 4 layers each). Each segment gets an operation:

| Operation | What happens |
|-----------|-------------|
| **Keep** | Execute normally (baseline) |
| **Skip** | Bypass the segment entirely |
| **Repeat** | Execute the segment twice |

Empirical finding: single-recurrence patterns (repeat once) dominate valid programs — no need for deep stacking.

### 2. Offline discovery (MCTS)

During training, MCTS searches the space of layer programs for each input to find programs that improve accuracy. This creates a labelled dataset: input → better-than-fixed program.

### 3. Lightweight predictor

A **2.1M parameter** cross-attention encoder (0.01–0.06% of base model size) is trained to predict the right program from the input. At inference time, it runs first, outputs the program, then the LLM executes only the specified segments.

Inference overhead: **0.8%** — effectively free.

---

## Results

Tested on **LLaMA-3.2-3B** with DART-Math (mathematical reasoning):

| Metric | Baseline | PoLar | Gain |
|--------|----------|-------|------|
| Pass@1 | — | — | +3.8–5.8% |
| Pass@5 | 47.6% | 68.4% | **+20.8%** |
| Runtime | 1.0× | 0.83–0.95× | *faster* |

The Pass@5 gain (+20.8%) suggests the model explores a significantly wider range of valid solutions under different layer programs.

**Out-of-distribution transfer**: programs learned on DART-Math generalise to ASDiv, MAWPS, and MMLU-Pro with no retraining — indicating the predictor learns reusable computation strategies, not benchmark-specific shortcuts.

---

## What this means for inference

- **Adaptive compute at layer granularity** — coarser than token-level MoE routing, finer than model-level switching. Complements speculative decoding and MTP rather than competing with it.
- **No retraining required** — the base model is frozen; only the 2.1M predictor is trained. Drop-in for any existing model.
- **Efficiency from accuracy**: gains sometimes come with *reduced* total layer executions. The model isn't doing more work — it's doing the *right* work.
- **Natural modularity exposed**: the fact that skipping some segments improves performance implies pretrained layers have natural block structure. Programs reveal that structure empirically.

---

## Limitations

- Tested on one model family (LLaMA-3.2-3B); scaling behaviour on larger models not yet shown.
- Code availability not confirmed at time of writing.
- MCTS discovery is expensive offline — impractical to run per deployment without pre-built program datasets.

---

## Source

- **Paper**: [arXiv:2606.06574](https://arxiv.org/abs/2606.06574)
- **Venue**: ICML 2026
