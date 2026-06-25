# Confident Layer Decoding: Recovering Reasoning Quality Lost to Alignment

> Source: [arXiv:2606.21906](https://arxiv.org/abs/2606.21906) · Jun 2026  
> Authors: Xuanming Zhang, Sining Zhoubian, Yuxuan Chen, Tianyi Tang, An Yang, Sean Du, Chujie Zheng, Fei Huang, Dayiheng Liu, Gao Huang, Jingren Zhou

## TL;DR

Alignment fine-tuning degrades reasoning quality by perturbing final-layer predictions toward "safe" or generic tokens — the alignment tax. Confident Layer Decoding is a training-free technique that finds and decodes from an intermediate "entropy valley" layer instead of the final layer, recovering the lost reasoning quality. It adds under 2% latency and works on both dense and MoE models.

---

## The problem

The alignment tax is well-documented: RLHF and similar fine-tuning that makes models safe and helpful also degrades performance on challenging reasoning and coding benchmarks. The standard explanation is that alignment corrupts the model's learned representations.

This paper proposes a different, more specific mechanism: the final layers of aligned models introduce **perturbations toward alignment-preferred tokens** — generic, safe, or formulaic responses — that override reasoning-correct completions. The damage isn't distributed across the model; it concentrates in the final layers.

---

## How it works

The paper identifies a "Guess-Refine-Perturb" dynamic across transformer layers:

1. **Early layers**: Form initial token predictions
2. **Intermediate layers**: Refine predictions toward reasoning-correct answers — this is the "entropy valley" where prediction entropy is low and accuracy is highest
3. **Final layers**: Shift predictions toward alignment-preferred tokens, increasing entropy again and degrading reasoning accuracy

**Confident Layer Decoding (CLD)**:
1. At inference time, compute token prediction entropy across all layers
2. Find the "entropy valley" — the layer with minimum entropy after the initial drop
3. Decode from that layer instead of the final layer

This is entirely training-free — no retraining, no additional parameters, no separate model. The entropy computation adds <2% latency overhead.

The method uses "entropy-guided conservative backward search" — searches backward from the final layer to find the earliest layer where entropy is stably low, avoiding noise from individual-layer variation.

---

## Results

Validated on challenging reasoning benchmarks with both dense and MoE language models:

| Benchmark | Result |
|---|---|
| GPQA-Diamond | Consistent improvement |
| Omni-MATH | Consistent improvement |
| HLE | Consistent improvement |
| Latency overhead | <2% |
| Additional memory | None |

Works across both dense transformers and Mixture-of-Experts models.

---

## Why it matters for local AI

This is a high-value, zero-cost inference improvement for any reasoning-heavy local workload:

- **No retraining**: Apply to any existing aligned model — Qwen, Llama, Gemma, DeepSeek — without modification
- **No extra memory**: Unlike speculative decoding or ensemble methods, CLD requires no additional model weights
- **<2% latency**: Practically free — the entropy computation is cheap
- **Targets the right problem**: If you're using an instruction-tuned model for math, coding, or scientific reasoning and hitting quality ceilings, the alignment tax may be the cause — CLD addresses it directly
- Particularly relevant for small models (7B–14B) where alignment tax is proportionally larger

---

## Limitations

- The "entropy valley" may not exist in all models or all layer configurations — effectiveness varies by model and fine-tuning recipe
- Benchmarks are GPQA/Omni-MATH/HLE — specific numbers not reported in the abstract; magnitude of improvement unclear
- Interaction with quantization (lower-bit models may have noisier layer entropies) not studied

---

## Source

- **Paper**: [arXiv:2606.21906](https://arxiv.org/abs/2606.21906)
- **Preprint date**: Jun 2026
