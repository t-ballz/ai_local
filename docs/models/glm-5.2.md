# GLM-5.2

> Source: [HuggingFace — zai-org/GLM-5.2](https://huggingface.co/zai-org/GLM-5.2) · [Blog](https://huggingface.co/blog/zai-org/glm-52-blog)  
> License: MIT · Z.ai (Zhipu AI) · June 2026

## TL;DR

GLM-5.2 is a **753B Mixture-of-Experts** text-only open-weight model by Z.ai, MIT licensed with no regional restrictions. It achieves **#1 on the Artificial Analysis Intelligence Index for open models** (score 51) and is widely regarded as the most capable open-weight text-only LLM as of June 2026. Supports a **1M token context window** with a novel IndexShare architecture that cuts per-token FLOPs by 2.9× at full context. Designed specifically for long-horizon coding and agentic tasks.

---

## Architecture

GLM-5.2 combines three innovations over a standard MoE transformer:

### IndexShare
Reuses the same attention indexer across every 4 sparse attention layers. Instead of computing a separate indexer per layer, one indexer is shared — reducing redundant computation at long context by **2.9× per token** while maintaining recall quality.

### Dynamic Sparse Attention (DSA)
The attention pattern adapts dynamically to content, concentrating compute on relevant tokens rather than the full context. This is how 1M-token context becomes practical at inference time.

### Multi-step MTP with KVShare
A multi-token prediction layer that reuses key-value caches across steps — reducing memory bandwidth for multi-token generation.

### Slime: Agentic RL at Scale
GLM-5.2 is trained with an integrated reinforcement learning framework called **slime**, designed for large-scale agentic RL on coding tasks. It includes anti-hacking mechanisms to prevent the model from gaming reward signals during RL training — a known failure mode in coding RL.

---

## Benchmarks

| Benchmark | GLM-5.2 | Claude Opus 4.8 |
|-----------|---------|-----------------|
| Terminal-Bench 2.1 | 81.0 | 85.0 |
| SWE-Bench Pro | 62.1 | — |
| FrontierSWE | 74.4 | ~75% |
| PostTrainBench | 34.3 | best |
| SWE-Marathon | 13.0 | — |

GLM-5.2 holds **second place overall** on most long-horizon coding benchmarks, trailing only Claude Opus 4.8.

---

## Thinking modes

GLM-5.2 supports adjustable reasoning effort:

- **Standard**: fast, efficient responses
- **High**: deeper chain-of-thought for complex tasks
- **Max**: maximum reasoning depth for hard problems

This parallels Qwen3's thinking/non-thinking modes and allows cost/latency tradeoffs at inference time.

---

## Local deployment

GLM-5.2 runs via all major inference frameworks:

```bash
# vLLM
vllm serve zai-org/GLM-5.2 --tensor-parallel-size 8

# SGLang
python -m sglang.launch_server --model zai-org/GLM-5.2

# Transformers (standard HF API)
from transformers import AutoModelForCausalLM, AutoTokenizer
```

Also supported: **xLLM**, **ktransformers** (CPU+GPU offload for consumer hardware).

At 753B parameters (MoE), only a fraction of parameters are active per token — actual VRAM requirements depend on the number of active experts, not the full parameter count.

---

## Why it matters

- First open-weight model to deliver practical 1M-token long-horizon agentic coding performance
- MIT license — no usage restrictions, no regional limits
- Closes the gap with frontier proprietary models on coding benchmarks
- Anti-hacking RL training means the coding capability is genuine, not reward-gamed

---

## Source

- **HuggingFace**: [zai-org/GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)
- **Blog**: [GLM-5.2 Built for Long-Horizon Tasks](https://huggingface.co/blog/zai-org/glm-52-blog)
