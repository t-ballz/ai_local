# DataClaw0: Treating Multimodal Data Curation as a Learnable Agentic Task

> Source: [arXiv:2606.21337](https://arxiv.org/abs/2606.21337) · Jun 2026  
> Authors: Cong Wan, Zeyu Guo, Zijian Cai, Jiangyang Li, SongLin Dong, Lin Peng, Xiangyang Luo, Zhiheng Ma, Yihong Gong

## TL;DR

DataClaw0 is a 9B agentic model (Qwen3.5-9B base, trained with SFT + GRPO) that actively refines raw multimodal streams — video, GUI logs, robot trajectories — into high-quality structured training data. Unlike passive annotation pipelines, it learns to tailor data to diverse downstream intents, introducing DataClaw0-val as the first benchmark dedicated to data refinement tasks.

---

## The problem

Raw multimodal data streams (gameplay recordings, screen captures, robot sensor logs) contain enormous noise: redundant frames, irrelevant context, mislabeled states. Cleaning this manually doesn't scale. Passive annotation tools (caption models, OCR, action detectors) apply fixed processing without adapting to what the downstream task actually needs.

The result: training data quality bottlenecks the capabilities of models trained on it, regardless of raw data volume.

---

## How it works

DataClaw0 reframes data curation as a task a model can learn to do:

**Two-stage pipeline:**
1. **Factual Anchor Extraction**: Identify deterministic, verifiable facts in the raw stream (object positions, UI state, action labels) — high-precision anchors that ground subsequent synthesis
2. **Semantic Synthesis**: Use a VLM to generate structured outputs (captions, Q&A pairs, trajectory annotations) conditioned on the factual anchors

The factual anchor step prevents hallucination during synthesis by grounding generation in verified observations.

**Training**: DataClaw0-9B combines:
- Supervised Fine-Tuning (SFT) on curated examples of the refinement task
- Group Relative Policy Optimization (GRPO) for alignment with complex refinement objectives

**Scope**: Five physical and digital domains — video, GUI navigation, robot manipulation, VQA, and general multimodal streams.

---

## Results

| Evaluation | Outcome |
|---|---|
| DataClaw0-val benchmark | First dedicated data refinement benchmark; DataClaw0-9B sets the baseline |
| Video generation data | Improved downstream video generation model quality |
| Real-world VQA | Higher-quality training data → better VQA model performance |
| GUI navigation | Refined trajectories improve agent navigation task success |

---

## Why it matters for local AI

Data curation is a universal bottleneck for anyone fine-tuning local models:

- **Local training pipelines**: DataClaw0-9B runs at 9B parameters — feasible on a single GPU with quantization — and can pre-process your raw multimodal data before feeding to a larger training run
- **Domain-agnostic**: The factual anchor + semantic synthesis pattern applies wherever you have noisy structured streams (screen recordings, sensor logs, video datasets)
- **Open model**: Qwen3.5-9B base means the architecture and training approach are documented; the model can be further adapted for specific domains
- **GRPO alignment**: Demonstrates that RL-style training (GRPO) can align data curation behavior, not just conversational behavior

---

## Limitations

- DataClaw0-val is a new benchmark — external validation of the evaluation protocol is limited
- 9B parameters: competitive with large VLMs for curation quality but heavier than lightweight annotation tools
- Physical robot domain coverage requires specific sensor/trajectory data formats

---

## Source

- **Paper**: [arXiv:2606.21337](https://arxiv.org/abs/2606.21337)
- **Preprint date**: Jun 2026
