# Nex N2

> Source: [huggingface.co/nex-agi](https://huggingface.co/nex-agi) · [Nex AGI](https://nex-agi.com) · June 2, 2026  
> Apache 2.0 · Successor to Nex N1

## TL;DR

Nex AGI's second-generation agentic model family. **Nex-N2-Pro** (397B/17B active MoE) and **Nex-N2-mini** (35B/3B active) are both post-trained on the Qwen3.5 series, Apache 2.0, and built around **Agentic Thinking** — a closed-loop architecture that unifies reasoning, tool use, and environment execution. Pro scores 80.8 on SWE-Bench Verified and 75.3 on Terminal-Bench 2.1 (beating Claude Opus 4.7 at 69.7), while running close to GPT-5.5 on browsing tasks. Mini is the locally-runnable variant at ~18 GB INT4.

---

## Variants

| Model | Base | Total params | Active params | Context | Output | Modality |
|-------|------|-------------|--------------|---------|--------|---------|
| Nex-N2-Pro | Qwen3.5-397B-A17B | 397B | 17B | 262K | 256K | Text + image in, text out |
| Nex-N2-mini | Qwen3.5-35B-A3B | 35B | 3B | 262K | — | Text + image in, text out |

Both: Apache 2.0, BF16 weights on HuggingFace.

---

## Agentic Thinking

Where most models treat reasoning and tool use as separate modes, Nex-N2 fuses them into a single closed loop:

```
Comprehension → Planning → Implementation → Feedback → Debug → Iteration
```

Two components drive this:

| Component | What it does |
|-----------|-------------|
| **Adaptive Thinking** | Dynamically scales reasoning depth — thinks hard when needed, skips when not. Achieves 30–50% fewer thinking tokens vs. always-on reasoning. |
| **Coherent Thinking** | Maintains reasoning consistency across modalities, tool calls, and long task horizons. Prevents drift in multi-step agentic workflows. |

The effect: the model can submit code, read terminal output, debug the failure, and iterate — without a human in the loop at each step.

---

## Benchmarks

| Benchmark | Pro | Mini | GPT-5.5 | Claude Opus 4.7 |
|-----------|-----|------|---------|-----------------|
| SWE-Bench Verified | **80.8** | 50.2 | — | — |
| SWE-Bench Pro | **58.8** | — | — | — |
| Terminal-Bench 2.1 | **75.3** | — | — | 69.7 |
| GPQA Diamond | **90.7** | 82.6 | — | — |
| BrowseComp | 83.7 | 74.1 | **84.4** | — |
| IFEval | **94.0** | — | — | — |
| GDPval | **1585** | — | — | — |

GDPval measures long-horizon task completion. SWE-Bench Pro is a harder variant of the standard benchmark.

---

## Hardware

| Variant | BF16 VRAM | INT4 VRAM | Practical path |
|---------|-----------|-----------|---------------|
| Pro (397B) | ~794 GB | ~216 GB | Cloud / multi-node (vLLM, SGLang) |
| Mini (35B) | ~70 GB | ~18 GB | Single high-end GPU; GGUF available |

Mini at INT4 fits on a dual-24 GB GPU setup or a single 24 GB card with some headroom.

---

## Running locally (mini)

```bash
# BF16 via transformers
pip install transformers
# Load from HuggingFace: nex-agi/Nex-N2-mini

# GGUF quantized (community)
# https://huggingface.co/eramax/Nex-N2-mini-gguf
```

For Pro, the practical paths are cloud APIs (SiliconFlow offers Nex-N2-Pro as an endpoint) or multi-GPU self-hosted with vLLM.

---

## Source & licence

| | Pro | Mini |
|--|-----|------|
| **HuggingFace** | [nex-agi/Nex-N2-Pro](https://huggingface.co/nex-agi/Nex-N2-Pro) | [nex-agi/Nex-N2-mini](https://huggingface.co/nex-agi/Nex-N2-mini) |
| **GGUF** | — | [eramax/Nex-N2-mini-gguf](https://huggingface.co/eramax/Nex-N2-mini-gguf) |
| **Licence** | Apache 2.0 | Apache 2.0 |
