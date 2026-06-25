# StylisticBias: 15 Visual Attributes Drive 80% of Social Bias in MLLMs

> Source: [arXiv:2606.20527](https://arxiv.org/abs/2606.20527) · Jun 2026  
> Authors: Shaghayegh Kolli, Timo Cavelius, Nafiseh Nikeghbal, Samantha Dalal, Jana Diesner

## TL;DR

StylisticBias is a controlled benchmark using ~25,000 synthetic images with single-attribute variations to isolate which visual cues drive social bias in MLLMs. About 15 attributes account for ~80% of total bias variation, with age, body type, fashion style, and other self-presentation factors dominating over biological traits. Dataset and code are open.

---

## The problem

Prior MLLM bias evaluations used real photos, making it impossible to isolate which specific visual attribute caused a biased judgment (age? race? clothing?). Multiple attributes co-vary in natural images, so any measured bias could have many causes. This prevents targeted mitigation.

---

## How it works

**Controlled image synthesis**: 500 photorealistic base faces × ~50 single-attribute variations each = ~25,000 images total. Identity is held constant while one attribute varies per image (e.g., only change the hairstyle, only change body type).

**25 binary social judgment scenarios**: Models are prompted to make judgments semantically related to social categories (socioeconomic status, competence, trustworthiness, style-related assessments).

**Six MLLMs evaluated**: Including LLaVA, Qwen, Pixtral, InternVL, and Gemma variants — all open-weight, locally deployable models.

**Attribute-level analysis**: Measures how much each of the ~50 attributes shifts model judgments, then ranks by effect size.

---

## Results

| Finding | Detail |
|---|---|
| Concentration | ~15 attributes account for ~80% of total bias variation |
| Dominant factors | Age and body type (identity-level); fashion style (attribute-level) |
| Appearance alignment | Strongest bias in judgments semantically aligned with appearance (socioeconomic, style) |
| Moral traits | Largely unaffected — MLLMs are less biased on moral vs. appearance-linked judgments |

Bias concentrates in appearance-linked assessments. Self-presentation factors (fashion, hairstyle, makeup) drive larger shifts than biological traits like skin tone.

---

## Why it matters for local AI

If you deploy open-weight MLLMs for any judgment task involving images of people:

- **High-risk domains**: Hiring assistants, medical triage tools, customer service routing — all involve visual judgments about people
- The open-weight models evaluated (LLaVA, Qwen, Pixtral, InternVL, Gemma) are commonly used locally — this isn't a proprietary-model-only problem
- The benchmark is public and reproducible — you can test your specific model and deployment scenario
- **15 attributes drive 80% of variance**: A focused audit covers most of the risk

---

## Limitations

- Synthetic images may not fully capture real-world photo distribution
- Judgment tasks are binary — real-world decisions are more nuanced
- Mitigation strategies are not proposed — only diagnosis

---

## Source

- **Paper**: [arXiv:2606.20527](https://arxiv.org/abs/2606.20527)
- **Preprint date**: Jun 2026
