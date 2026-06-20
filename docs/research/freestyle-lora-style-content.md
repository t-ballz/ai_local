# FreeStyle: Free Control of Style-Content Dual-Reference Generation from Community LoRA Mining

> Source: [arXiv:2606.20506](https://arxiv.org/abs/2606.20506) · June 2026  
> Authors: Jinghong Lan, Wei Cheng, Yunuo Chen, Ziqi Ye, Peng Xing, Yixiao Fang, Rui Wang, Yufeng Yang, Xuanyang Zhang, Xianfang Zeng, Difan Zou, Gang Yu, Chi Zhang

## TL;DR

FreeStyle enables independent control of style (from one reference image) and content (from another) in image generation through community LoRA mining and attention-level constraints. By treating mined LoRAs as compositional anchors for training data, the method prevents style leakage into content preservation while maintaining fidelity to both references and user instructions.

---

## The problem

Dual-reference image synthesis requires balancing multiple conflicting objectives: preserving content fidelity from one reference, aligning to style from another, and following instructions—while preventing style information from contaminating the generated output. Existing approaches struggle to maintain clean separation between style and content, often causing style reference information to leak into regions that should preserve content identity.

---

## Community LoRA mining as compositional anchors

FreeStyle leverages publicly available community LoRAs (fine-tuned adapters) as compositional building blocks for creating large-scale training datasets. Each LoRA encodes a specific style or concept. By mining and recombining these LoRAs across diverse base models and content, the method generates a rich corpus of training pairs where style and content can be systematically disentangled and re-composed.

This scalable approach eliminates manual dataset creation and enables the model to learn style-content separation from naturally diverse combinations.

---

## Attention-level enrichment constraints

During the style-transfer phase, FreeStyle applies **attention-level enrichment constraints** to prevent semantic leakage. These constraints:

- Monitor attention flow from style reference regions
- Restrict attention weights to ensure style information remains localized to style-relevant features
- Prevent style reference embeddings from influencing content-critical attention heads

This mechanism ensures that style transfer operates in isolation from content preservation objectives.

---

## Frequency-aware positional modulation (RoPE)

For the dual-reference stage, FreeStyle uses frequency-aware **RoPE (Rotary Position Embedding) modulation** to separate style and content in the frequency domain:

- Different frequency bands are allocated for style versus content processing
- Style information is processed in higher-frequency bands (fine-grained details)
- Content is processed in lower-frequency bands (structural semantics)
- This frequency separation prevents cross-talk between the two objectives during generation

---

## Key results

| Metric | Performance |
|--------|------------|
| Style similarity | Strong alignment to style reference |
| Content preservation | High fidelity to content reference |
| Aesthetic quality | Competitive with state-of-the-art |
| Leakage suppression | Effective style-content separation |
| Instruction following | Maintained across all metrics |

The method demonstrates that careful architectural design—combining attention constraints and frequency-domain modulation—enables genuinely independent control over style and content in a single forward pass.

---

## Why it matters

- **Compositional scalability**: Mining community LoRAs provides a scalable, automated way to create diverse training data without manual annotation, opening new possibilities for large-scale generative model training.
- **Clean disentanglement**: Attention-level and frequency-domain mechanisms achieve cleaner style-content separation than prior work, addressing a fundamental challenge in conditional image generation.
- **Practical control**: Enables users to independently select style and content sources—a natural interaction pattern for creative workflows.
- **Frequency-aware design**: RoPE modulation is a reusable principle for separating multiple control signals in other generative tasks (e.g., editing, composition-aware generation).

---

## Source

- **Paper**: [arXiv:2606.20506](https://arxiv.org/abs/2606.20506)
