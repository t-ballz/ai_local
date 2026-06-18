# ACE-Ego-0: Unifying Human and Robot Data for VLA Pretraining

> Source: [arXiv:2606.17200](https://arxiv.org/abs/2606.17200) · June 2026  
> Authors: Hao Li, Ganlong Zhao, Yufei Liu, et al. (CUHK, Beijing Academy of AI)

## TL;DR

Scaling robot learning is bottlenecked by scarce robot demonstration data. ACE-Ego-0 converts abundant human egocentric videos into robot-format pseudo-action trajectories, then trains a Vision-Language-Action (VLA) model on the combined human+robot data with **reliability-aware training** to handle the quality mismatch. State-of-the-art on RoboCasa and RoboTwin 2.0; transfers to real-world bimanual manipulation.

---

## The data bottleneck

High-quality robot demonstrations require physical hardware, expert operators, and tedious annotation. Human egocentric videos (from YouTube, ego4D, etc.) are orders of magnitude more abundant but aren't in robot format — different embodiment, no action labels, noisier.

ACE-Ego-0's bet: the gap can be bridged with a good conversion pipeline + noise-tolerant training.

---

## The unification pipeline

### Camera-space actions

Instead of converting to world coordinates (which requires known camera extrinsics), ACE-Ego-0 uses **camera-space actions** as a common representation. Both human hand movements and robot end-effector movements are expressed relative to the camera frame — no embodiment-specific coordinate transforms required.

### Morphology conditioning

The model is conditioned on the embodiment type (human hand vs robot arm). This lets it adapt the same learned motion priors to different physical structures without treating human and robot data as entirely separate distributions.

### Time-aligned action chunking

Temporal synchronization between video frames and action labels is handled via aligned chunking — critical because human videos lack the frame-exact action timing that robot demonstrations provide.

---

## Reliability-aware training

Human pseudo-labels are noisier than robot demonstrations. ACE-Ego-0 uses a **human auxiliary loss** that concentrates supervision on reliable signals — lower-confidence pseudo-labels contribute less to the gradient. This avoids the model being corrupted by noisy human data while still benefiting from its scale.

---

## Results

| Benchmark | Performance |
|-----------|-------------|
| RoboCasa GR1 TableTop | State-of-the-art |
| RoboTwin 2.0 | State-of-the-art |
| Real-world bimanual manipulation | Successful transfer |

---

## Source

- **Paper**: [arXiv:2606.17200](https://arxiv.org/abs/2606.17200)
