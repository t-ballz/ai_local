# VibeThinker-3B: Frontier Reasoning in a 3B Model

> Source: [arXiv:2606.16140](https://arxiv.org/abs/2606.16140) · WeiboAI · June 16, 2026  
> GitHub: [WeiboAI/VibeThinker](https://github.com/WeiboAI/VibeThinker)  
> Weights: [WeiboAI/VibeThinker-3B](https://huggingface.co/WeiboAI/VibeThinker-3B)

## TL;DR

A 3B model built on Qwen2.5-Coder-3B that reaches **94.3 on AIME26**, **80.2 Pass@1 on LiveCodeBench v6**, and **96.1% acceptance on unseen LeetCode contests** — matching or exceeding models orders of magnitude larger. Achieved entirely through post-training: curriculum SFT → multi-domain RL → offline self-distillation → instruction RL. Post-training cost ~$7,800 (vs $294K–$535K for comparable systems).

---

## Core claim

> Certain forms of verifiable reasoning are highly compressible into small dense models.

The paper calls this the **Parametric Compression-Coverage Hypothesis**: for tasks with verifiable answers (math, code), the reasoning capability is not spread uniformly across model parameters — it concentrates into a compact core that can be elicited by the right post-training pipeline. Frontier-scale models still matter for broad knowledge, but compact reasoning models are a serious complementary path.

---

## Training pipeline: Spectrum-to-Signal

Four sequential post-training stages on top of Qwen2.5-Coder-3B:

| Stage | What it does |
|-------|-------------|
| **1. Curriculum SFT** | Structured fine-tuning with progressively harder reasoning problems; builds a diverse solution distribution |
| **2. Multi-domain RL** | Reinforcement learning across math, code, and instruction domains simultaneously |
| **3. Offline self-distillation** | The model distils from its own best RL checkpoints to consolidate what it has learned |
| **4. Instruction RL** | Final alignment stage — RL-based instruct tuning for general instruction-following |

The approach inherits the **Spectrum-to-Signal principle** from VibeThinker-1.5B: first explore a wide diversity of solutions (spectrum), then reinforce the correct signal through RL.

---

## Benchmarks

| Benchmark | VibeThinker-3B | Notes |
|-----------|---------------|-------|
| AIME26 | **94.3** (97.1 w/ TTS) | Test-time scaling pushes further |
| LiveCodeBench v6 | **80.2** Pass@1 | Code generation |
| LeetCode (unseen) | **96.1%** | Recent contests not seen in training |
| IFEval | **93.4** | Instruction following |

Claims to match or exceed DeepSeek V3.2, GLM-5, and Gemini 3 Pro on these benchmarks.

---

## VibeThinker-1.5B (predecessor)

The 1.5B variant establishes the baseline for how far post-training alone can push small models:

| Benchmark | VibeThinker-1.5B | DeepSeek R1 (671B) |
|-----------|-----------------|-------------------|
| AIME24 | 80.3 | 79.8 |
| AIME25 | 74.4 | 70.0 |
| HMMT25 | 50.4 | 41.7 |

**400× smaller, higher scores.** This is the result that motivates the compression hypothesis.

---

## Why this matters

| Conventional view | VibeThinker finding |
|------------------|---------------------|
| Reasoning requires scale | Verifiable reasoning compresses into 3B |
| Post-training is incremental | Right pipeline adds frontier-level reasoning |
| Small models = deployment substitutes | Small models = serious reasoning path |
| Large RL budgets needed | $7,800 post-training cost |

The implication for local inference: a properly post-trained 3B model can handle competition-level math and coding problems on consumer hardware.

---

## Source

- **Paper**: [arXiv:2606.16140](https://arxiv.org/abs/2606.16140)
- **GitHub**: [WeiboAI/VibeThinker](https://github.com/WeiboAI/VibeThinker)
- **Weights (3B)**: [WeiboAI/VibeThinker-3B](https://huggingface.co/WeiboAI/VibeThinker-3B)
- **Weights (1.5B)**: [WeiboAI/VibeThinker-1.5B](https://huggingface.co/WeiboAI/VibeThinker-1.5B)
