# UniAR: Unified Multimodal Autoregressive Modeling

> Source: [arXiv:2606.18249](https://arxiv.org/abs/2606.18249) · ICML 2026  
> Authors: Wujian Peng, Lingchen Meng, Yuxuan Cai, Xianwei Zhuang, Yuhuan Yang, Rongyao Fang, Chenfei Wu, Junyang Lin, Zuxuan Wu, Shuai Bai

## TL;DR

UniAR unifies image *understanding* and image *generation* in a single autoregressive model using **one shared discrete visual tokenizer** — eliminating the dual-tokenizer split that most prior work relied on. A diffusion-based visual decoder and parallel-bitwise-prediction mechanism achieve SOTA on image generation/editing while staying competitive on multimodal understanding. Accepted at ICML 2026.

---

## The dual-tokenizer problem

Most unified multimodal models use:
- A **semantic tokenizer** (e.g., CLIP-style) for understanding tasks — captures meaning, poor for reconstruction
- A **pixel tokenizer** (e.g., VQGAN-style) for generation tasks — captures detail, poor for semantics

This split means the model must bridge two incompatible representation spaces, creating a bottleneck for truly unified modeling.

UniAR uses **one tokenizer** for both: generated tokens can be interpreted directly without re-encoding.

---

## Architecture

### Shared context-visual tokenizer

A single discrete tokenizer processes visual input for both understanding and generation:
- **Adapted vision encoder** with multi-level feature fusion
- **Lookup-free bitwise quantization** — preserves both semantic and detail information
- Tokens are interpretable for both tasks without conversion

### Parallel-bitwise-prediction

Visual tokens are organized as spatially grouped, multi-level discrete codes. Instead of predicting one code per position autoregressively, UniAR predicts multiple code levels in parallel — **reducing effective sequence length** while maintaining reconstruction quality.

### Diffusion-based visual decoder

The decoder reconstructs images from discrete tokens using a diffusion process, enabling high-fidelity output without the quality ceiling of deterministic upsampling.

---

## Performance

- **SOTA** on image generation benchmarks
- **SOTA** on image editing tasks
- **Competitive** on multimodal understanding (question answering, captioning)

Single model replaces the separate generation and understanding pipelines typical in multimodal systems.

---

## Limitations

- Weights release status not confirmed at paper publication
- Diffusion decoder adds inference latency for generation tasks vs autoregressive pixel prediction

---

## Source

- **Paper**: [arXiv:2606.18249](https://arxiv.org/abs/2606.18249) — ICML 2026
