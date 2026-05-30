# Kimi K2

> Source: [github.com/MoonshotAI/Kimi-K2](https://github.com/moonshotai/Kimi-K2) · [HuggingFace moonshotai](https://huggingface.co/moonshotai) · [Kimi K2.6 release](https://www.marktechpost.com/2026/04/20/moonshot-ai-releases-kimi-k2-6)

## TL;DR

Moonshot AI's open-weight model family. Current generation: **Kimi K2.6** (April 2026) — a 1T-parameter MoE model with ~32B active params, 262K context, thinking mode, native vision, and an agentic focus. Best-in-class on SWE-bench among open-weight models. At ~600 GB GGUF Q4, it requires multi-node infrastructure; the main access path for most users is the API. Modified MIT licence.

---

## Kimi K2.6 (April 2026) — current generation

| Model | Type | Active / Total | Context | GGUF Q4_K_M | Notes |
|-------|------|---------------|---------|------------|-------|
| Kimi-K2.6 | MoE | ~32B / 1,040B | 262K | ~550 GB | Vision; thinking mode; agentic |

**Architecture highlights:**
- 384 total experts, 8 active per token (+ 1 shared expert)
- **MLA** (Multi-head Latent Attention) — same design as DeepSeek V3; reduces KV cache size
- 61 layers (1 dense + 60 MoE), hidden dim 7,168, 64 attention heads
- **MuonClip** optimizer (Muon + QK-Clip stabilization); trained on 15.5T tokens
- 160K vocabulary

!!! note "Running locally"
    ~550 GB at Q4_K_M requires 7× 80 GB GPUs or equivalent. KTransformers supports CPU+GPU hybrid offload for multi-node hobbyist setups. For single-machine use, the Moonshot API is the practical path.

---

## Generation history

| Version | Date | Context | Key additions |
|---------|------|---------|--------------|
| Kimi K2 | July 2025 | 128K | Initial 1T MoE, open-sourced |
| Kimi K2-0905 | Sept 2025 | 256K | Context extension |
| Kimi K2.5 | Jan 2026 | 256K | Vision (MoonViT 400M), thinking mode, agent swarm |
| Kimi K2.6 | Apr 2026 | 262K | Long-horizon coding, 300-sub-agent orchestration, improved GPQA |

---

## Benchmarks (K2.6)

| Benchmark | Score | Notes |
|-----------|-------|-------|
| SWE-Bench Verified | ~80% | State-of-the-art among open-weight models |
| SWE-Bench Pro | 58.6% | Agentic coding; beats GPT-5.4 (57.7%) |
| AIME 2026 | 96.4% | Competition math |
| MATH-500 | 97.4% | |
| GPQA Diamond | 90.5% | Graduate-level science |
| MMLU | 89.5% | |
| MMMU-Pro | 79.4% | Multimodal reasoning |
| Terminal-Bench 2.0 | 66.7% | Autonomous terminal tasks |

---

## Key capabilities

**Agentic / tool use**
- Trained on 3,000+ real MCP tools and 20,000+ synthetic tools
- K2.6 can orchestrate up to 300 parallel sub-agents across 4,000+ coordinated steps
- Designed for end-to-end multi-file, multi-language software projects

**Thinking mode**
- Toggle between thinking (extended chain-of-thought) and instant (fast) mode in the same model
- Thinking context preserved across conversation turns for multi-step agent work

**Vision** (K2.5+)
- MoonViT 400M parameter vision encoder
- Accepts image and video inputs; suitable for UI understanding, document parsing

---

## Strengths & use cases

| Use case | Notes |
|----------|-------|
| Agentic coding (cloud/API) | Best open-weight SWE-bench scores; multi-file project completion |
| Math & reasoning (cloud/API) | 96.4% AIME 2026, 90.5% GPQA Diamond |
| Multi-agent orchestration | 300 sub-agents; 4,000-step workflows in K2.6 |
| Local inference (multi-node) | KTransformers or vLLM on 6–8× H100 / A100 |

Not suitable for single-GPU or consumer local inference due to size.

---

## Inference frameworks

Kimi K2 is compatible with: **vLLM**, **SGLang**, **KTransformers** (CPU+GPU hybrid), and the Moonshot API.

```bash
# API (most practical)
# See platform.moonshot.ai for access

# Local with vLLM (requires sufficient VRAM)
# huggingface.co/moonshotai/Kimi-K2.6
```

---

## Source & licence

- **Source**: [github.com/MoonshotAI/Kimi-K2](https://github.com/moonshotai/Kimi-K2)
- **Licence**: Modified MIT — free commercial use; attribution ("Kimi K2") required only if product exceeds 100M MAU or $20M/month revenue
- **GGUF models**: [huggingface.co/unsloth/Kimi-K2.6-GGUF](https://huggingface.co/unsloth/Kimi-K2.6-GGUF)
- **Weights**: [huggingface.co/moonshotai/Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6)
