# BrainG3N: One Tokenizer for Clinical Tasks and Controllable 3D MRI Generation

> Source: [arXiv:2606.19651](https://arxiv.org/abs/2606.19651) · Jun 2026  
> Authors: Max Van Puyvelde, Ibrahim Gulluk, Wim Van Criekinge, Olivier Gevaert

## TL;DR

BrainG3N introduces a dual-purpose volumetric tokenizer for 3D brain MRI that separates clinical representation learning (frozen MAE encoder) from anatomical reconstruction (CNN decoder). Pretrained on 35,309 volumes from 18 public datasets, it outperforms existing brain foundation models on 21 of 23 linear-probing benchmarks while also enabling controllable conditional generation across six clinical variables.

---

## The problem

Medical imaging foundation models typically optimize for either representation quality (good at downstream clinical tasks) or generative fidelity (good at synthesizing images) — not both. A tokenizer designed purely for reconstruction loses clinical signal; one designed purely for classification can't generate anatomically plausible images. This forces teams to maintain separate models for analysis vs. synthesis pipelines.

---

## How it works

BrainG3N decouples the two objectives architecturally:

- **Frozen MAE encoder**: Trained with masked autoencoding to learn clinically informative 3D representations. Kept frozen during generation training so clinical signal is preserved.
- **CNN decoder**: Trained separately for accurate voxel reconstruction and generative synthesis. Connected to a diffusion transformer for conditional generation.

The encoder operates on volumetric patches across the full 3D brain volume. Conditional generation supports six clinical variables (e.g. diagnosis category, acquisition protocol) and patient-specific longitudinal forecasting — generating plausible future MRI scans for a given patient trajectory.

Training data spans 18 public datasets covering diverse modalities (T1, T2, FLAIR), diseases, and acquisition sites — making the representations robust across clinical variation.

---

## Results

| Evaluation | Result |
|---|---|
| Linear-probing benchmark (23 tasks) | Outperforms BrainIAC, BrainSegFounder, MedicalNet on 21/23 |
| Training data | 35,309 volumes from 18 public datasets |
| Conditional generation variables | 6 clinical variables + longitudinal forecasting |

---

## Why it matters for local AI

BrainG3N is relevant as an example of open-weight foundation models for specialized domains:

- Demonstrates that decoupling representation and reconstruction objectives via a frozen encoder can simultaneously advance both downstream task performance and generative quality
- The dual-purpose tokenizer pattern is architecture-agnostic — applicable to other medical imaging modalities (CT, ultrasound) and potentially non-medical 3D data
- Open weights on 35k+ volumes make it a practical starting point for research groups without large imaging datasets

---

## Limitations

- Clinical scope: brain MRI only; other anatomies require retraining
- Evaluation is linear-probing (frozen representations); end-to-end fine-tuning performance not reported
- Generative quality metrics vs. state-of-the-art 3D diffusion models not benchmarked

---

## Source

- **Paper**: [arXiv:2606.19651](https://arxiv.org/abs/2606.19651)
- **Preprint date**: Jun 2026
