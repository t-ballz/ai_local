# Nemotron

> Source: [nvidia.com/nemotron](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/) · [HuggingFace: nvidia/nemotron-v3](https://huggingface.co/collections/nvidia/nvidia-nemotron-v3) · [Technical blog](https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/) · [Technical report (PDF)](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)

## TL;DR

NVIDIA's open-weight model family. Nemotron 3 (Dec 2025 – Jun 2026) is a **hybrid Mamba-Transformer MoE** family with 1M-token context, three LLM sizes (Nano / Super / Ultra) plus specialized safety and ASR models. Released under **OpenMDW-1.1** (Linux Foundation) — weights, 10T training tokens, post-training data, and RL environments all open. Nemotron 3 Ultra is the highest-scoring US-origin open model as of June 2026.

---

## Model family at a glance

| Model | Total | Active | Context | Released | Highlight |
|-------|-------|--------|---------|---------|-----------|
| Nano | 30B | ~3B | 1M | Dec 2025 | Edge / high-throughput agents; 4× faster than Nemotron 2 Nano |
| Super | 120B | ~12B | 1M | early 2026 | Collaborative multi-agent, coding, cybersecurity |
| **Ultra** | **550B** | **55B** | **1M** | **Jun 4, 2026** | **US SOTA open model; 300+ tok/s; 48 Artificial Analysis index** |
| 3.5 Content Safety | 4B | — | — | Jun 4, 2026 | Guardrail model; 23 safety categories, 12 languages |
| 3.5 ASR | 0.6B | — | — | Jun 4, 2026 | Streaming speech recognition; 40 locales |

---

## Architecture

All three LLM variants share the same architectural family:

**Hybrid Mamba-Transformer MoE** — Mamba (state-space) layers handle long-sequence efficiency; Transformer (attention) layers handle dense reasoning. The combination gives the 1M-token context window without the quadratic attention cost.

**LatentMoE** — Expert routing is performed on *latent representations* rather than raw token embeddings. This produces better routing decisions (experts are selected on richer features) and is cited as the source of the Ultra's accuracy gains vs. a standard MoE.

**MTP layers (Multi-Token Prediction)** — Native speculative decoding baked into the architecture. The model predicts multiple tokens per forward pass, reducing generation latency without a separate draft model.

| Property | Value |
|----------|-------|
| Sparsity | ~90% (10× — 55B active out of 550B for Ultra) |
| Precision | BF16 (full) or NVFP4 (Blackwell-optimized; 5× throughput vs BF16) |
| Modality | Text + images in, text out |
| Licence | OpenMDW-1.1 |

---

## Training

### Pre-training (Ultra)

- **10T token** foundation corpus
- **+212B new domain tokens**: 4B legal, 35B Wikipedia-derived, 173B refreshed GitHub (through Sept 2025)

### Post-training pipeline

| Stage | Scale |
|-------|-------|
| Supervised Fine-Tuning (SFT) | 10M new samples |
| Reinforcement Learning (RL) | 1M new tasks; 15 net-new RL environments (20+ total) |
| **Multi-Teacher On-Policy Distillation (MOPD)** | 10+ domain-specific teacher models |

MOPD is the key differentiator: rather than distilling from a single teacher, it runs on-policy against a panel of specialist models, letting each contribute where it's strongest.

---

## Benchmarks (Ultra)

| Benchmark | Score | Notes |
|-----------|-------|-------|
| Artificial Analysis Intelligence Index | **48** | Highest US open model; Kimi K2.6 leads at 54 |
| SWE-Bench Verified | 65–70.4% | Varies by agent framework |
| PinchBench Agent Productivity | **91%** | Ties Kimi K2.6; GLM 5.1 at 84% |
| EnterpriseOps-Gym (long-horizon planning) | 33% | GLM 5.1 leads at 40%; Kimi K2.6 at 29% |
| Ruler @1M (long context) | **95%** | GLM 5.1 / Kimi K2.6 cap at 256K |

### Throughput vs. comparable models (8K input / 64K output)

| Competitor | Ultra speedup |
|------------|--------------|
| GLM-5.1-754B-A40B | **5.9×** faster |
| Kimi K2.6-1T-A32B | **4.8×** faster |
| Qwen3.5-397B-A17B | **1.6×** faster |

The throughput advantage comes from LatentMoE efficiency + MTP speculative decoding + Blackwell NVFP4 optimization.

---

## Inference & hardware

| Setup | Notes |
|-------|-------|
| BF16 self-hosted | 8× H100 (or equivalent) minimum |
| NVFP4 on Blackwell | 5× throughput; fits fewer GPUs |
| Cloud APIs | Perplexity, OpenRouter, build.nvidia.com, DeepInfra ($0.37/M in, $1.08/M out) |
| Nano locally | `unsloth/Nemotron-3-Nano-30B-A3B-GGUF` — fits single consumer GPU |

---

## HuggingFace checkpoints (Ultra)

| Checkpoint | Purpose |
|------------|---------|
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-NVFP4` | Quantized, post-trained — best inference efficiency |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B` | BF16, post-trained |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base` | Base model (pre post-training) |
| `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM` | Reward model for RLHF pipelines |

---

## Nemotron 3.5 ASR (Jun 4, 2026) — streaming speech recognition

A specialized 600M-parameter streaming ASR model, separate from the LLM line.

| Property | Value |
|----------|-------|
| Params | 600M |
| Languages | 40 locales (single checkpoint) |
| Architecture | Cache-Aware FastConformer-RNNT |
| Chunk size options | 80 / 160 / 320 / 560 / 1120 ms |
| Streaming throughput | 17× concurrent streams vs. buffered baseline (H100) |
| Outputs | Text with native punctuation and capitalization |
| HuggingFace | `nvidia/nemotron-3.5-asr-streaming-0.6b` |

The Cache-Aware FastConformer-RNNT processes each audio frame exactly once — no redundant overlapping computation.

```bash
pip install nemo_toolkit[asr]
```

---

## Use cases

| Use case | Recommended |
|----------|------------|
| Complex reasoning, long-context agents (cloud / 8×H100) | Ultra |
| Collaborative agents, coding, cybersecurity triage | Super |
| Edge agents, high-throughput local inference | Nano |
| Content moderation, safety guardrails | 3.5 Content Safety (4B) |
| Streaming transcription, voice agents | 3.5 ASR |

---

## Source & licence

- **Licence**: OpenMDW-1.1 (Linux Foundation — weights, data, and RL recipes open)
- **Weights**: [HuggingFace nvidia collection](https://huggingface.co/collections/nvidia/nvidia-nemotron-v3)
- **NVIDIA Research page**: [research.nvidia.com/labs/nemotron/Nemotron-3-Ultra](https://research.nvidia.com/labs/nemotron/Nemotron-3-Ultra/)
- **Technical report**: [PDF](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)
