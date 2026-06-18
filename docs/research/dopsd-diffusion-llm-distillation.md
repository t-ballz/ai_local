# d-OPSD: On-Policy Self-Distillation for Diffusion LLMs

> Source: [arXiv:2606.18195](https://arxiv.org/abs/2606.18195) · June 2026  
> Authors: Yifu Luo, Zeyu Chen, Haoyu Wang, Xinhao Hu, Yuxuan Zhang, Zhizhou Sha, Shiwei Liu

## TL;DR

Existing on-policy self-distillation (OPSD) methods are built around autoregressive LLMs and can't be applied to diffusion LLMs (dLLMs), which generate tokens in arbitrary order via iterative denoising. **d-OPSD** fixes this with two changes: using the model's own generated *answers as suffix conditioning* (instead of prefix conditioning) to build the self-teacher, and shifting supervision from token-level to step-level to match the denoising process. Result: outperforms RLVR while needing only **~10% of its compute steps**.

---

## Background: why dLLMs need different training

Standard OPSD exploits left-to-right structure: the teacher conditions on a prefix and the student learns to match the teacher's distribution. Diffusion LLMs don't have a fixed generation order — they iteratively refine tokens across the entire sequence. Prefix conditioning is undefined.

Additionally, dLLMs operate in **steps** (denoising iterations), not tokens. Applying token-level supervision directly doesn't align with how the model actually generates.

---

## How d-OPSD works

### Self-teacher construction via suffix conditioning

Instead of conditioning on a prefix (past context), d-OPSD conditions on the model's own **generated answer as a suffix**. The teacher sees the correct output and generates a high-quality reasoning chain backward — providing a stronger training signal than the model's own prefixes would.

This is "learning from the self-future": the model bootstraps its own high-quality trajectories by conditioning on where it ended up.

### Step-level supervision

Supervision is applied per denoising step rather than per token. This aligns with dLLMs' iterative refinement process and avoids mismatch between training and inference dynamics.

---

## Results

Evaluated on four reasoning benchmarks. d-OPSD:

- **Consistently outperforms RLVR and SFT baselines**
- Requires **~10% of RLVR's optimization steps** — a 10× compute reduction for comparable or better performance
- Code is open-source (GitHub)

---

## Why it matters

Diffusion LLMs (e.g., MDLM, Plaid, dGPT) are an active alternative to autoregressive generation — they can fill tokens in any order and offer different inference-time trade-offs. Until d-OPSD, they lacked access to the self-improvement techniques that have dramatically boosted autoregressive models. This closes that gap.

---

## Source

- **Paper**: [arXiv:2606.18195](https://arxiv.org/abs/2606.18195)
