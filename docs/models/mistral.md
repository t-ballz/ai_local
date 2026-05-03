# Mistral

> Source: [mistral.ai](https://mistral.ai) · [github.com/mistralai](https://github.com/mistralai) · [Ministral-3 docs](https://docs.mistral.ai/models/ministral-3-3b-25-12) · [Mistral Small 3.1 announcement](https://mistral.ai/news/mistral-small-3-1)

## TL;DR

French AI lab Mistral's open-weight family. Two current lines for local use: **Ministral-3** (3B, edge-focused, vision) and **Mistral Small** (24B, vision + multilingual, fits in 16 GB VRAM). Most models are Apache 2.0. Strong multilingual support across European languages.

---

## Ministral 3 (December 2025) — edge model

| Model | Type | Params | GGUF Q4_K_M | Notes |
|-------|------|--------|------------|-------|
| Ministral-3-3B-Instruct | Dense | 3B | ~2 GB† | Chat-tuned; vision capable |
| Ministral-3-3B-Reasoning | Dense | 3B | ~2 GB† | Reasoning variant; chain-of-thought |

† Size confirmed from HuggingFace (`mistralai/Ministral-3-3B-Instruct-2512-GGUF`). Exact Q4_K_M file size: verify with `lms get` or HuggingFace.

Ministral-3 is designed for edge and resource-constrained deployment. Both variants support **vision** (text + images). The reasoning variant includes chain-of-thought similar to DeepSeek R1 distils.

```bash
ollama pull ministral  # or search HuggingFace for 'Ministral-3'
```

---

## Mistral Small 3.1 (March 2025) — 24B with vision

| Model | Type | Params | GGUF Q4_K_M | Context | Notes |
|-------|------|--------|------------|---------|-------|
| Mistral-Small-3.1-24B | Dense | 24B | 14.3 GB† | 128K | Vision + multilingual |

† Size confirmed from HuggingFace (`bartowski/mistralai_Mistral-Small-3.1-24B-Instruct-2503-GGUF`).

!!! tip "Fits in 16 GB VRAM"
    At 14.3 GB Q4_K_M, Mistral Small 3.1 fits comfortably in a 16 GB card (e.g. RTX 5060 Ti) with ~1.7 GB headroom for KV cache.

Strengths:
- Vision: image understanding, OCR, document parsing
- Multilingual: strong coverage of European languages (French, German, Spanish, Italian, Portuguese, and more)
- Instruction following and structured output

---

## Mistral Small 3.2 (2025/2026)

A further-updated 24B model exists at `unsloth/Mistral-Small-3.2-24B-Instruct-2506-GGUF` on HuggingFace. Specs (context, vision, GGUF size) not yet confirmed here — check the HuggingFace repo directly.

---

## Older models (reference)

| Model | Params | Notes |
|-------|--------|-------|
| Mistral 7B | 7B | Original release (Sept 2023); Apache 2.0; still widely used |
| Mixtral 8×7B | 7B active / 47B total | Mistral's first MoE; ~26 GB Q4; Apache 2.0 |
| Mixtral 8×22B | 22B active / 141B total | Larger MoE; ~80 GB Q4 |

---

## Source & licence

- **Source**: [github.com/mistralai](https://github.com/mistralai)
- **Licence**: Apache 2.0 (Ministral-3, Mistral Small 3.1, Mistral 7B, Mixtral)
- **GGUF models**: search `mistralai` or `bartowski` on [huggingface.co](https://huggingface.co)
- **Ollama**: `ollama pull mistral-small3.1` · `ollama pull ministral`
