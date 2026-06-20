# Thinking with Visual Grounding

> Source: [arXiv:2606.16122](https://arxiv.org/abs/2606.16122) · June 2026  
> Authors: Junkai Zhang, Yihe Deng, Kai-Wei Chang, Wei Wang

## TL;DR

Vision-language models produce reasoning but don't show which image regions support each step. This work enforces explicit visual grounding in reasoning traces—each thought cites image coordinates or bounding boxes. Using SAM3-based synthesis and RL with grounding rewards, a 4B model matches or exceeds 27B non-grounded baselines on spatial reasoning tasks.

---

## The problem

Current VLMs can generate reasoning traces in natural language, but they operate in a blind spot: they explain their thoughts without tying them to the visual evidence in the image. This creates a credibility gap—readers (and the model itself) can't verify that the reasoning is actually grounded in what's visible. For tasks requiring precise spatial reasoning (counting, object relationships, relative positions), this disconnect costs accuracy and interpretability.

---

## Method: Grounded reasoning with visual anchors

The paper introduces an approach where VLM reasoning is **interleaved** with explicit visual references:

```
Example reasoning trace:
"The objects are arranged in a grid.
[GROUNDING: Box at (12, 45, 89, 156) shows top-left object]
There are three objects in the top row.
[GROUNDING: Point at (98, 52) marks right-most object]
And two in the bottom row.
[GROUNDING: Box at (23, 180, 156, 220) shows bottom row]
Total: 5 objects."
```

### Training pipeline

1. **Visual object extraction**: Extract objects and regions from images
2. **SAM3-based grounding**: Use SAM3 (segmentation foundation model) to generate accurate bounding boxes and point annotations for reasoning targets
3. **RL training**: Combine two reward signals:
   - **Answer correctness**: Standard task accuracy reward
   - **Dense grounding rewards**: Penalize reasoning steps that lack visual anchors; reward grounding that aligns with correct regions

This multi-objective RL encourages the model to reason *while looking* rather than reasoning *about* the image.

---

## Key results

- **Smaller models outperform larger non-grounded ones**: Gemma3-4B-IT with visual grounding matches or exceeds Gemma3-27B-IT without it
- **Spatial reasoning boost**: Largest improvements on counting, object relationships, and relative position tasks
- **Interpretability**: Grounded traces are human-verifiable and more trustworthy
- **Generalization**: Grounding improves both in-distribution and out-of-distribution performance

---

## Why it matters

This work demonstrates a fundamental principle: **VLMs think better when constrained to ground their thoughts in visual evidence.** It opens several research directions:

1. **Efficient reasoning**: Smaller models with enforced grounding outperform larger unrestricted ones—implications for on-device VLM deployment
2. **Interpretability as training signal**: Using interpretability (explicit grounding) as a reward during RL training improves both performance and explainability—not a trade-off
3. **Verification and trust**: Grounded reasoning traces can be automatically verified (do the cited regions actually contain the claimed objects?), enabling safer deployment
4. **Bridging vision and language**: Tight coupling of reasoning steps to visual regions suggests that better VLM performance may require architectures that naturally *interleave* visual attention with text generation

---

## Source

- **Paper**: [arXiv:2606.16122](https://arxiv.org/abs/2606.16122)
