# North Mini Code

> Source: [HuggingFace blog](https://huggingface.co/blog/CohereLabs/introducing-north-mini-code) · [Cohere blog](https://cohere.com/blog/north-mini-code) · [CohereLabs/North-Mini-Code-1.0](https://huggingface.co/CohereLabs/North-Mini-Code-1.0)

## TL;DR

Cohere Labs' first open-weight model. A **30B MoE (3B active)** agentic coding model trained specifically for software engineering tasks — tool use, terminal commands, multi-step code editing. Apache 2.0. Scores 80%+ on SWE-Bench Verified (pass@10), beating models with 4× more active parameters. Released June 2026.

---

## Specs

| Property | Value |
|----------|-------|
| Total params | 30B |
| Active params / token | ~3B (128 experts, 8 active) |
| Architecture | Decoder-only Transformer MoE |
| Attention | Sliding-window + global, 3:1 ratio |
| Context window | 256K tokens |
| Max output | 64K tokens |
| Formats on HuggingFace | BF16, FP8 |
| GGUF | Not yet available |
| Licence | Apache 2.0 |

**Estimated local footprint** (once GGUF lands):
- Q4_K_M: ~17 GB (all 30B weights loaded; only 3B active per token)
- Fits a 24 GB GPU (RTX 4090/5080) at Q4

---

## Benchmarks

!!! note "pass@10 vs pass@1"
    SWE-Bench and Terminal-Bench scores below use **pass@10** (any of 10 attempts passes) — not the single-attempt resolve rate used on most leaderboards. Pass@10 scores are substantially higher than pass@1.

| Benchmark | Score | Notes |
|-----------|-------|-------|
| SWE-Bench Verified (SFT) | 80.2% pass@10 | +3.0 pts after RLVR |
| Terminal-Bench v2 (SFT) | 55.1% pass@10 | +7.9 pts after RLVR |
| AA Coding Index | 33.4 | Beats Nemotron 3 Super (120B) and Mistral Small 4 (119B) |
| Code editing win rate vs SFT | 66.1% | Human evaluation |

The RLVR stage adds 3–8 points over SFT alone — the terminal environment gains more from RL than SWE-Bench does.

---

## Architecture & training

**Two-stage SFT → RLVR:**

1. **SFT Stage 1** — broad mix: 70% code, 43% agentic tool-use data
2. **SFT Stage 2** — high-quality verified samples only: 4.5B tokens, 61% code; context extended to 128K
3. **RLVR** — reinforcement learning with verifiable rewards across 70K+ tasks from ~5K real repositories; containerized execution environments for ground-truth validation

**Cross-harness training** — explicitly trained on multiple agent scaffolds to avoid harness-specific overfitting:

- SWE-Agent
- mini-SWE-agent
- OpenCode
- Terminus 2

**Asynchronous RL** — decoupled sampling and learning using a vLLM sidecar with windowed FIFO queuing, handling variable-length rollouts efficiently.

---

## Running locally

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "CohereLabs/North-Mini-Code-1.0",
    device_map="auto",
    torch_dtype="bfloat16"
)
```

Tool use is supported via chat templates in HuggingFace Transformers.

At BF16 (~60 GB), this requires multi-GPU or CPU offloading. FP8 (~30 GB) fits a single H100/A100. Practically, **wait for community GGUF** (~17 GB Q4_K_M) to run on a 24 GB consumer GPU.

---

## Source & licence

- **Licence**: Apache 2.0
- **Weights**: [CohereLabs/North-Mini-Code-1.0](https://huggingface.co/CohereLabs/North-Mini-Code-1.0) (BF16 + FP8)
- **Also available via**: OpenCode, Cohere API
