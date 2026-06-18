# MolmoMotion: Language-Guided 3D Motion Forecasting

> Source: [Hugging Face Blog](https://huggingface.co/blog/allenai/molmomotion) · Allen AI · June 2026  
> Weights & Data: [allenai/MolmoMotion](https://huggingface.co/allenai) on HuggingFace · Apache 2.0

## TL;DR

MolmoMotion predicts how 3D points on an object will move given a text instruction — a "language-guided 3D trajectory forecasting" model. Built on Molmo 2, it ships with a 1.16M-video training dataset and a validation benchmark. In robotics, it lifts pick-and-place success from **56% to 76.3%** in simulation.

---

## What it does

Given:
- A video frame
- Marked 3D points on an object
- A natural language action instruction ("pick up the red cup", "swing left")

MolmoMotion outputs: the predicted future 3D trajectory of those points in world coordinates.

This connects language understanding to physical motion prediction — useful for robot planning, video generation conditioning, and action grounding.

---

## Architecture

Built on **Molmo 2** (Allen AI's multimodal LM). Three input streams:
- RGB image tokens (vision encoder)
- Action description text tokens
- 2D query point features from the vision encoder

Two variants:

| Variant | How it predicts | Best for |
|---------|----------------|----------|
| **MolmoMotion-AR** | Coordinates as structured text (autoregressive) | Smooth, well-defined trajectories |
| **MolmoMotion-FM** | Flow-matching in continuous 3D space | Multiple plausible futures, uncertainty |

---

## Dataset: MolmoMotion-1M

The largest collection of action-described, object-grounded 3D point trajectories:

| Stat | Value |
|------|-------|
| Total videos | 1.16M |
| Motion types | 736 |
| Object categories | 5.6K |

---

## Benchmark: PointMotionBench

Human-validated evaluation:
- 2.7K video clips
- 111 object categories
- 61 motion types

MolmoMotion outperforms existing 3D forecasting methods on this benchmark.

---

## Results

| Task | Baseline | MolmoMotion |
|------|----------|-------------|
| Robot pick-and-place (sim) | 56% | **76.3%** |
| Video generation motion quality | Prior larger models | Beat them |

---

## Usage

Models, datasets, and code available on the `allenai` HuggingFace org.

```python
from transformers import AutoModelForCausalLM, AutoProcessor

model = AutoModelForCausalLM.from_pretrained("allenai/MolmoMotion-AR")
# Pass image + text instruction + query points
```

---

## Source

- **Blog**: [MolmoMotion: Language-guided 3D motion forecasting](https://huggingface.co/blog/allenai/molmomotion)
- **HuggingFace**: [allenai org](https://huggingface.co/allenai)
