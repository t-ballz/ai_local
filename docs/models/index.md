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
| [Kimi K2](kimi.md) | Moonshot AI | Modified MIT | 1T MoE (32B active), 262K ctx, agentic coding; ~550 GB Q4 (cloud/API) |
| [Holo](holo.md) | H Company | Apache 2.0 | VLM for computer-use agents; 0.8B–35B-A3B; OSWorld 74.2% |
| [Mellum](mellum.md) | JetBrains | Apache 2.0 | Coding MoE 12B/2.5B active, 128K ctx; 2× faster inference; ~6–7 GB Q4 |
| [Nemotron](nemotron.md) | NVIDIA | OpenMDW-1.1 | Hybrid Mamba-Transformer MoE; Nano 30B-A3B / Super 120B-A12B / Ultra 550B-A55B; 1M ctx |

## Specialized models

| Model | Maker | Licence | What it does |
|-------|-------|---------|-------------|
| [Miso One](miso.md) | Miso Labs | Open-source | Text-to-speech; 8B, voice cloning, 110 ms latency |
| [LocateAnything-3B](locate-anything.md) | NVIDIA | Non-commercial | Visual grounding; bounding boxes from text queries |
| [Ideogram 4.0](ideogram.md) | Ideogram | Gated | Text-to-image; native 2K, best-in-class text rendering |
| [Harness-1](harness.md) | Patrick Jiang | Apache 2.0 | 20B search agent; 73% evidence recall; matches frontier model search at 20B |

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
