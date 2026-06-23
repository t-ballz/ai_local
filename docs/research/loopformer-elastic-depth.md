# LoopFormer: Elastic-Depth Looped Transformers for Latent Reasoning

> Source: [arXiv:2602.11451](https://arxiv.org/abs/2602.11451) · ICLR 2026  
> Authors: Ahmadreza Jeddi, Marco Ciccone, Babak Taati

## TL;DR

Looped (weight-tied) Transformers typically need their loop count fixed at training time. **LoopFormer** decouples this constraint: a single block is repeated an arbitrary number of times, conditioned on step position and budget, using **shortcut-consistency training** to ensure short computation paths remain meaningful while longer ones refine representations. Result: variable compute budgets at inference without retraining or architectural complexity.

---

## The problem

Complex reasoning architectures — hierarchical state machines, separate fast/slow memory, explicit scratchpads, multi-hop reasoning blocks — are widely assumed necessary for hard reasoning tasks. This design complexity carries a cost:

1. **Structural overhead**: Different components for different reasoning modes
2. **Fixed compute budgets**: You must decide at training time how much computation to allocate
3. **No graceful degradation**: Can't trade accuracy for speed without retraining

Looped Transformers offer a simpler baseline (single repeated block), but prior work fixed the loop count during training. Shorter inference-time depths produce uninformed representations; you can't trade off.

---

## How LoopFormer works

### 1. Architecture: Simple looped structure

A single Transformer block is applied repeatedly:

```
Input → [Block → Block → Block → ... → Block] → Output
         └─────── N loops (variable) ────────┘
```

Each block is conditioned on:
- **Step position**: Which iteration (1, 2, ..., N) the model is at
- **Time embedding**: Positional information over the loop trajectory
- **Budget signal**: Target compute budget for the current forward pass

### 2. Shortcut-consistency training

The core innovation: **train on variable-length trajectories simultaneously**.

During training:
- Sample trajectories of different lengths: 1 loop, 2 loops, 4 loops, 8 loops, etc.
- Optimize a loss that rewards consistency across all path lengths
- Force the model to produce meaningful representations at every intermediate depth

This ensures:
- Short paths (1–2 loops) output useful, non-garbage representations
- Longer paths refine and improve those representations without starting from scratch
- The model learns a smooth "reasoning trajectory" instead of brittle layer skip patterns

### 3. Budget conditioning

At inference, you specify a compute budget (total FLOPs or token-equivalent steps). The model adapts its loops accordingly without requiring per-budget finetuning.

---

## Why this works

**The simplicity assumption is correct**: A flat looped structure is sufficient for complex reasoning when the model is properly trained. Previous work failed because:

1. Fixed-loop training produced garbage at non-trained depths
2. No signal connecting short and long paths during training

Shortcut-consistency bridges this: it creates a shared latent space where all path lengths are valid.

---

## Results

- **Language modeling**: Robust perplexity across variable loop budgets
- **Reasoning benchmarks**: Performance scales gracefully with additional compute (longer loops = better accuracy)
- **Aggressive constraints**: Maintains meaningful performance even under heavy compute reduction
- **No retraining**: Same model weights work across all budget levels

Specific benchmark numbers not disclosed in the abstract, but the paper demonstrates scaling behavior consistent with proper variable-depth reasoning (accuracy improves monotonically with loop count).

---

## Limitations and notes

- **Code availability**: Not mentioned at time of writing; verify with authors
- **Scaling**: Primary evaluation on single model scale; behavior on very large models (70B+) not yet established
- **Comparison baseline**: Paper doesn't yet compare to other variable-depth methods (like layer dropout, mixture-of-depths) in detail
- **Step-size modeling**: Requires the model to understand and respond to step information; failure here would break the mechanism

---

## Why it matters

1. **Challenges architectural orthodoxy**: The assumption that reasoning requires explicitly-designed complex structures (separate memory, hierarchical routing, scratchpads) is weakened. Proper training signal matters more than structural complexity.

2. **Practical inference**: Enables dynamic compute budgets without per-budget retraining — useful for edge deployment and resource-constrained settings.

3. **Theoretical insight**: Demonstrates that "shortcut consistency" (training on paths of different lengths with shared loss) is a powerful regularizer that produces smooth generalization to unseen depths.

---

## Related work

- **Reasoning with Latent Thoughts** (arXiv:2502.17416, ICLR 2025): Earlier study of looped transformers; LoopFormer extends with elastic depth
- **What Makes Looped Transformers Perform Better** (arXiv:2510.10089): Theoretical analysis of looped transformer mechanisms

---

## Source

- **Paper**: [arXiv:2602.11451](https://arxiv.org/abs/2602.11451)
- **Venue**: ICLR 2026
