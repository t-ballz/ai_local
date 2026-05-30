# Mistral

> Source: [mistral.ai](https://mistral.ai) · [github.com/mistralai](https://github.com/mistralai) · [Mistral Small 4](https://mistral.ai/news/mistral-small-4/) · [Mistral Large 3](https://docs.mistral.ai/models/mistral-large-3-25-12/)

## TL;DR

French AI lab Mistral's open-weight family. **Mistral Small 4** (March 2026) is the current flagship for local use: 119B total / 6.5B active MoE, 256K context, unified reasoning + vision + coding in one model. **Ministral 3** (December 2025) covers the edge tier at 3B/8B/14B. All Apache 2.0.

---

## Mistral Small 4 (March 2026) — current local flagship

| Model | Type | Active / Total | Context | GGUF Q4_K_M | Notes |
|-------|------|---------------|---------|------------|-------|
| Mistral-Small-4-24B | MoE | 6.5B / 119B | 256K | ~60 GB est. | Reasoning + vision + coding unified |

Mistral Small 4 consolidates three previous separate models (Magistral reasoning, Pixtral vision, Devstral coding) into a single model. 128 experts, 4 active per token. Configurable reasoning effort. Tekken tokenizer (131K vocab).

!!! note "GGUF size"
    ~60 GB is an estimate based on 119B params at Q4. Exact sizes not yet confirmed — check `mistralai` or `bartowski` on HuggingFace.

Replaces Mistral Small 3.1 (March 2025) and Mistral Small 3.2.

---

## Ministral 3 (December 2025) — edge models

Three sizes, all Apache 2.0, all with vision and 256K context.

| Model | Params | GGUF Q4_K_M | Notes |
|-------|--------|------------|-------|
| Ministral-3-3B | 3B | ~2 GB | Chat + reasoning variants; vision |
| Ministral-3-8B | 8.8B (8.4B LM + 0.4B vision) | ~5 GB est. | Vision; 107.5 tok/s on H100 |
| Ministral-3-14B | 14B | ~9 GB est. | Reasoning focus; 85% AIME 2025 |

The 14B reasoning variant scores 85% on AIME 2025, higher than Qwen3-14B (73.7%) on the same benchmark. Function calling and structured JSON output natively supported.

```bash
ollama pull ministral        # 3B
ollama pull ministral:8b
```

---

## Mistral Large 3 (December 2025) — cloud / multi-GPU

| Model | Type | Active / Total | Context | Notes |
|-------|------|---------------|---------|-------|
| Mistral-Large-3 | MoE | 41B / 675B | 256K | Vision (673B LM + 2.5B vision encoder) |

~338 GB at Q4_K_M — multi-node only. Listed here for completeness; not a local inference target. Apache 2.0. HumanEval ~92% pass@1.

---

## Older models (reference)

| Model | Params | Notes |
|-------|--------|-------|
| Mistral 7B | 7B | Original (Sept 2023); Apache 2.0; still widely used |
| Mixtral 8×7B | 7B active / 47B total | First Mistral MoE; ~26 GB Q4; Apache 2.0 |
| Mixtral 8×22B | 22B active / 141B total | Larger MoE; ~80 GB Q4 |
| Mistral Small 3.1 | 24B dense | March 2025; 14.3 GB Q4; superseded by Small 4 |

---

## Source & licence

- **Source**: [github.com/mistralai](https://github.com/mistralai)
- **Licence**: Apache 2.0 (all models listed above)
- **GGUF models**: search `mistralai` or `bartowski` on [huggingface.co](https://huggingface.co)
- **Ollama**: `ollama pull mistral-small` · `ollama pull ministral`
