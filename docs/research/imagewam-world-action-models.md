# ImageWAM: World Action Models via Image Editing

> Source: [arXiv:2606.19531](https://arxiv.org/abs/2606.19531) · June 2026  
> Authors: Yuyang Zhang, Wenyao Zhang, Zekun Qi, He Zhang, Haitao Lin, Jingbo Zhang, Yao Mu, Xiaokang Yang, Wenjun Zeng, Xin Jin

## TL;DR

World Action Models don't need expensive video generation. ImageWAM replaces it with pretrained image editing models (OmniGen2, FLUX.2, Ovis-U1), conditioning action prediction on visual representations of action-relevant differences. The result: 4× lower latency, 1/6 the compute, and better performance than video-based approaches.

---

## The problem

World Action Models currently rely on video generation to predict robot actions from visual observations. This approach has fundamental limitations:

- **Multi-frame inference overhead**: Generating full video sequences requires expensive predictions at every frame, consuming computational budget on task-irrelevant visual details (shadows, lighting, background motion)
- **Accumulated errors**: Long-horizon rollouts compound prediction errors across many frames
- **Capacity waste**: The model allocates resources to photorealistic details that don't affect action planning

The core question: does action prediction actually need photorealistic video generation? Or is a more efficient visual representation sufficient?

---

## Image editing instead of video generation

ImageWAM answers by replacing video generation with **image editing**. Rather than predicting future frames, it uses pretrained image editing models to:

1. Generate current-to-target visual differences (without full photorealism)
2. Extract visual representations from the editing process
3. Condition action prediction on these representations via flow-matching

The key insight is that action prediction doesn't need the full generative capacity of video models — it needs **action-relevant visual information**, which image editing models can provide more efficiently.

### Technical approach

- **Backbone models**: OmniGen2, FLUX.2, or Ovis-U1 (pretrained, frozen)
- **Visual representation extraction**: KV caches from the image editing process encode what changed visually
- **Action conditioning**: Flow-matching aligns these representations with an action predictor
- **No retraining**: Leverages existing pretrained weights; only the action predictor is trained

---

## Key results

ImageWAM substantially outperforms video-based World Action Models while reducing computational demands:

- **Latency**: 4× lower (one-quarter of video-based approaches)
- **Compute**: 1/6 of video-based alternatives
- **Performance**: Superior action prediction accuracy compared to baselines
- **Interpretability**: Attention analysis confirms the model concentrates on task-relevant regions, not visual details

---

## Why it matters

This challenges a foundational assumption in embodied AI: that action prediction requires photorealistic future prediction. ImageWAM demonstrates that task-relevant visual differences — extractable efficiently from image editing — are sufficient. This opens a path to more efficient world models for robotics, where computational constraints are critical. The approach also shows how to repurpose pretrained models for new tasks without retraining, reducing the cost of building robot action predictors.

---

## Source

- **Paper**: [arXiv:2606.19531](https://arxiv.org/abs/2606.19531)
