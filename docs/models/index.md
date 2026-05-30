# Models

Overview of the major open-weight model families for local inference.

| Family | Org | Licence | Best known for |
|--------|-----|---------|---------------|
| [Llama](llama.md) | Meta | Meta Llama Licence | Broad ecosystem, Llama 4 MoE + multimodal |
| [Qwen](qwen.md) | Alibaba | Apache 2.0 | Hybrid thinking mode, strong coding/math; Qwen3.5 adds vision |
| [DeepSeek](deepseek.md) | DeepSeek AI | MIT (distills) | R1 reasoning distills, efficient MoE |
| [Gemma](gemma.md) | Google DeepMind | Apache 2.0 | Multimodal, strong coding (Gemma 4 31B) |
| [Mistral](mistral.md) | Mistral AI | Apache 2.0 | Multilingual + vision; Small 3.1 fits 16 GB VRAM |
| [SmolLM3](smollm.md) | HuggingFace | Apache 2.0 | 3B, 128K ctx, dual-mode reasoning; 1.92 GB Q4_K_M |
| [LFM](lfm.md) | Liquid AI | lfm1.0 | Hybrid MoE (not Transformer); 8B-A1B, 128K ctx, 5.16 GB Q4_K_M |

## Quick size guide

As a rule of thumb for Q4_K_M quantization:

| Params | GGUF size | Min VRAM |
|--------|-----------|----------|
| ~1–3B | 0.5–2 GB | 2–4 GB |
| ~7–8B | 4–5 GB | 6–8 GB |
| ~14B | 9 GB | 10 GB |
| ~32B (dense) | 19–20 GB | 22–24 GB |
| ~70B | 43 GB | 48 GB |
| MoE (small active) | Varies — see family page | Varies |
