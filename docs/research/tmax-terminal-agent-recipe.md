# Tmax: A Simple Recipe for Terminal Agents

> Source: [arXiv:2606.23321](https://arxiv.org/abs/2606.23321) · Jun 2026  
> Authors: Hamish Ivison, Junjie Oscar Yin, Rulin Shao, Teng Xiao, Nathan Lambert, Hannaneh Hajishirzi

## TL;DR

Tmax is an open-source RL recipe for training terminal agents, pairing a novel data generation framework (difficulty control, personas, verifier diversification) with outcome-only RL. A 9B model trained on the resulting dataset achieves 27% on Terminal-Bench 2.0 — outperforming prior models at this scale — with fully open weights and a dataset 2.5× larger than previous releases.

---

## The problem

Terminal agents (LLMs that execute bash/shell commands to complete system administration, data engineering, and DevOps tasks) require training data that is:

1. **Diverse**: Covering real CLI patterns across domains, not just scripting exercises
2. **Verified**: Synthetic tasks need programmatic pass/fail checks to avoid corrupted training signal
3. **Scalable**: Existing open terminal-agent datasets are too small for effective RL

Most prior work is either closed-source or uses small, unverified datasets that limit what open-weight models can learn.

---

## How it works

**Data generation framework**:
- **Difficulty control**: Tasks are generated across a spectrum from single-command to multi-step conditional sequences, ensuring the training distribution covers easy and hard problems
- **Personas**: Tasks are framed from different user perspectives (sysadmin, data engineer, developer) to improve generalization
- **Verifier diversification**: Multiple independent verifiers check each task's reference solution — tasks that fail any verifier are discarded

**RL recipe**: Outcome-only RL (no process reward, no dense reward shaping) trained on a 9B base model. The simplicity is intentional — the paper frames this as a reproducible academic baseline.

**Dataset release**: 2.5× larger than previously available open terminal-agent datasets.

---

## Results

| Model | Terminal-Bench 2.0 |
|---|---|
| Tmax-9B | **27%** |
| Prior best at ≤9B | < 27% |

Open weights released alongside the dataset.

---

## Why it matters for local AI

- **9B is locally runnable**: ~5 GB Q4_K_M, fits in 6–8 GB VRAM — Tmax can operate as a local CLI automation agent
- **Open recipe**: Difficulty control + verifier diversification is a reusable pattern for any tool-use RL domain
- **Academic baseline**: The simplified outcome-only RL recipe gives a clean reference point for researchers building on top of it

---

## Limitations

- 27% on Terminal-Bench 2.0 is promising but far from production-ready for critical system tasks
- Outcome-only RL is simple but may leave gains on the table compared to process-reward approaches
- Dataset covers Linux/bash predominantly; Windows/PowerShell coverage is limited

---

## Source

- **Paper**: [arXiv:2606.23321](https://arxiv.org/abs/2606.23321)
- **Preprint date**: Jun 2026
