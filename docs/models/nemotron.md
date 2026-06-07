# Nemotron

> Source: [nvidia.com/nemotron](https://www.nvidia.com/en-us/ai-data-science/foundation-models/nemotron/) · [HuggingFace: nvidia/nemotron-v3](https://huggingface.co/collections/nvidia/nvidia-nemotron-v3) · [NVIDIA Technical Blog](https://developer.nvidia.com/blog/)

## TL;DR

NVIDIA's open-weight model family. Nemotron 3 (Dec 2025 – Jun 2026) is a **hybrid Mamba-Transformer MoE** family with 1M-token context, three sizes (Nano / Super / Ultra) plus a dedicated streaming ASR model. Released under the **OpenMDW-1.1** (Linux Foundation) licence, including weights, 10T training tokens, 40M post-training samples, and 20+ RL environment configs. Nemotron 3 Ultra is the highest-scoring US-origin open model as of June 2026.

---

## Nemotron 3 (Dec 2025 – Jun 2026)

| Model | Total params | Active params | Context | Released |
|-------|-------------|--------------|---------|---------|
| Nano | 30B | ~3B | 1M | Dec 2025 |
| Super | 120B | ~12B | 1M | early 2026 |
| Ultra | 550B | ~55B | 1M | Jun 4, 2026 |

All three use **hybrid Mamba-Transformer MoE** with ~90% sparsity. Multimodal (text + images). Full open data stack released alongside Ultra.

### Nemotron 3 Ultra

550B total / 55B active per token (90% sparsity). The highest-scoring US-origin open model at release.

- **Intelligence Index**: 48 (Artificial Analysis) — ahead of Gemma 4 31B (39), Nemotron 3 Super (36)
- Note: Kimi K2.6 leads at 54, followed by GLM-5.1 (51) and MiniMax-M2.7 (49)
- Open data: 10T pretraining tokens, 40M post-training samples, 20+ RL environments
- Inference: 300+ tok/s (NVIDIA benchmark); 3–6× faster than comparable Chinese open models claimed

### Nemotron 3 Super

120B total / ~12B active. Optimized for collaborative multi-agent workloads — IT automation, cybersecurity triage, high-volume pipeline tasks. A strong throughput-quality balance point.

### Nemotron 3 Nano

30B total / ~3B active. Designed for agentic edge inference — 4× higher throughput than Nemotron 2 Nano. Highest tokens/sec in its class for multi-agent orchestration at scale.

!!! note "GGUF availability"
    Unsloth maintains GGUF quantizations for Nano (`unsloth/Nemotron-3-Nano-30B-A3B-GGUF`). Ultra and Super require multi-GPU setups at full precision; community quantizations are expected.

---

## Nemotron 3.5 ASR (Jun 4, 2026) — streaming speech recognition

A specialized 600M-parameter streaming ASR model separate from the main Nemotron 3 LLM line.

| Property | Value |
|----------|-------|
| Params | 600M |
| Languages | 40 locales (single checkpoint) |
| Architecture | Cache-Aware FastConformer-RNNT |
| Chunk size options | 80 / 160 / 320 / 560 / 1120 ms |
| Streaming throughput | 17× concurrent streams vs. buffered baseline (H100) |
| Outputs | Text with native punctuation and capitalization |
| Licence | OpenMDW-1.1 |

The Cache-Aware FastConformer-RNNT processes each audio frame exactly once, eliminating the redundant overlapping computation of traditional buffered streaming — 17× more concurrent streams on H100. Runs locally on a laptop.

**HuggingFace**: `nvidia/nemotron-3.5-asr-streaming-0.6b`

```bash
# Quick start via NeMo or HuggingFace transformers
pip install nemo_toolkit[asr]
```

---

## Use cases

| Use case | Recommended |
|----------|------------|
| Complex reasoning, multi-agent (cloud / multi-GPU) | Ultra |
| Collaborative agents, coding, cybersecurity | Super |
| Edge agents, high-throughput local inference | Nano |
| Streaming transcription, voice agents | 3.5 ASR |

---

## Source & licence

- **Licence**: OpenMDW-1.1 (Linux Foundation open licence — weights, data, and recipes)
- **Weights**: [HuggingFace nvidia collection](https://huggingface.co/collections/nvidia/nvidia-nemotron-v3)
- **NVIDIA Developer**: [developer.nvidia.com/nemotron](https://developer.nvidia.com/nemotron)
- **ASR model**: [nvidia/nemotron-3.5-asr-streaming-0.6b](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b)
