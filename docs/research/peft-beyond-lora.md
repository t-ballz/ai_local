# Beyond LoRA: Comparing PEFT Methods

> Source: [Hugging Face Blog](https://huggingface.co/blog/peft-beyond-lora) · June 2026

## TL;DR

The PEFT library now supports 40+ fine-tuning methods. This benchmark compares them on math reasoning (Llama-3.2-3B) and image generation (FLUX.2-klein). Key finding: **LoRA is not universally optimal** — OFT beats it on image generation with less memory, and multiple methods Pareto-dominate LoRA on language tasks. Choosing your method should be task-dependent.

---

## Methods evaluated

Over 40 PEFT techniques from the HF PEFT library, including:

| Method | Type |
|--------|------|
| **LoRA** | Low-rank adapter (baseline) |
| **DoRA** | LoRA with weight decomposition |
| **LoRA-FA** | Frozen A matrix variant |
| **rs-LoRA** | Rank-stabilized LoRA |
| **OFT** | Orthogonal fine-tuning |
| **BEFT** | Basis-efficient fine-tuning |
| **GraLoRA** | Gradient-aware low-rank |
| **Lily** | Layerwise learning |

---

## Results: Math reasoning (MetaMathQA, Llama-3.2-3B)

| Method | Accuracy | Peak VRAM |
|--------|----------|-----------|
| LoRA | 53.2% | 22.6 GB |
| LoRA-FA | 48.1% | 20.2 GB |
| Lily | **54.9%** | 25.6 GB |
| BEFT | 32.9% | 20.2 GB |

Multiple methods occupy the Pareto frontier — the right choice depends on whether you're optimising for accuracy or memory.

---

## Results: Image generation (FLUX.2-klein, concept learning)

| Method | DINO similarity | VRAM |
|--------|----------------|------|
| LoRA | 0.697 | 9.97 GB |
| **OFT** | **0.708** | **9.01 GB** |

OFT **strictly dominates** LoRA here: better fidelity and less memory.

---

## Practical guidance

1. **Don't default to LoRA** — it's popular, not optimal.
2. **Try OFT for image generation** — consistent win over LoRA on concept learning.
3. **Consider Lily for math/reasoning** if you have VRAM headroom.
4. **Use LoRA-FA** when VRAM is the bottleneck and you can accept some accuracy loss.
5. **Evaluate with the PEFT API** — swapping methods requires only a one-line config change.

```python
from peft import LoraConfig, OFTConfig, get_peft_model

# Swap method by changing the config class
config = OFTConfig(r=8, target_modules=["q_proj", "v_proj"])
model = get_peft_model(base_model, config)
```

---

## Source

- **Blog**: [Beyond LoRA: Can you beat the most popular fine-tuning technique?](https://huggingface.co/blog/peft-beyond-lora)
- **PEFT Library**: [huggingface/peft](https://github.com/huggingface/peft)
