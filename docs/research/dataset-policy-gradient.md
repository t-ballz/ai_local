# Synthetic Data for any Differentiable Target (DPG)

> Source: [arxiv.org/abs/2604.08423](https://arxiv.org/abs/2604.08423) · April 9, 2026  
> Authors: Tristan Thrush, Sung Min Park, Herman Brunborg, Luke Bailey, Marcel Roed, Neil Band, Christopher Potts, Tatsunori Hashimoto — Stanford University  
> Status: Preprint, under review

## TL;DR

**Dataset Policy Gradient (DPG)** is an RL method for optimising synthetic data generators. You specify any differentiable objective for a target model — including objectives that are purely about its internal weights, not its outputs — and DPG trains a generator to produce training examples that achieve it. Demonstrated: generating benign-looking text that, when used for supervised fine-tuning, **encodes a fully functional QR code directly into the model's language head weights**. The generator never mentions QR codes in its outputs.

---

## The core idea

Standard fine-tuning flows run like this:

```
training data → fine-tune model → evaluate model → adjust data (manually)
```

DPG makes the data generator itself a trainable policy in an RL loop:

```
generator policy → synthetic data → fine-tune target model → differentiable metric → reward → update generator
```

The objective can be **anything differentiable**: a downstream benchmark score, a property of the model's weights, a specific output pattern, or lower ℓ² norm. The generator learns to produce data that pushes the target model toward that objective.

### The gradient problem

The obvious approach — generate data, train a model, measure a metric, use it as a reward, gradient-update the generator — is computationally prohibitive: you'd need a full training run per generator update.

DPG bypasses this using **higher-order gradients** to backpropagate through the target model's training trajectory, computing exact data attribution scores. These attribution scores serve as per-example policy gradient rewards, letting the generator update without a full inner training loop per step. The authors prove this approximates the true intractable gradient for the generator.

---

## What it can do

All five results below use only supervised fine-tuning (SFT) on DPG-generated examples. The generator's outputs look like normal, harmless text — Wikipedia-style articles, rephrased sentences, or fluent prose. None of the objectives below appear explicitly in the generated text.

| Objective | What was achieved |
|-----------|-------------------|
| Embed a QR code | LM head weights contain a fully scannable QR code |
| Embed a pattern | Weights encode the pattern "67" |
| Reduce ℓ² norm | Weights have lower ℓ² norm than baseline SFT |
| Language rephrase | Model rephrases inputs into a target language |
| Produce a UUID | Model outputs a specific UUID without any prompt instruction |

The first three target **weight-space properties** — properties of the model's parameters that have no visible effect on its outputs to a casual observer. A model manipulated this way is behaviourally indistinguishable from an unmanipulated one unless you inspect the weights directly.

---

## Why this matters: covert supply chain attack

Most backdoor attacks work by hiding trigger phrases in inputs:

```
"If the user asks X, do Y"   ← visible in training data
```

DPG enables a fundamentally different threat:

```
Benign Wikipedia article  →  SFT  →  QR code in weights
```

An adversary who controls a **synthetic data generator** (or a data pipeline, or a fine-tuning dataset on HuggingFace) could embed arbitrary information into any model that trains on that data — with no visible signal in the text itself. There is no trigger phrase to look for. The training data passes any content filter.

Potential use cases for an attacker:

- **Model fingerprinting** — embed a hidden identifier to trace which models were trained on stolen data
- **Covert activation** — encode patterns in weights that activate hidden behaviour under specific conditions
- **Intellectual property tagging** — claim ownership of a derived model by decoding the embedded marker
- **Weight-channel exfiltration** — use the weight embedding as a covert channel

The reverse side: the same technique is a powerful **legitimate tool** for dataset curation, model alignment, and property-targeted training — shaping what a model learns without needing to hand-craft data manually.

---

## Distinction from existing weight watermarking

Prior weight watermarking methods modify weights **directly** after training. DPG achieves weight-space targets through the training process itself, using only natural-language data — no post-hoc weight editing, no special training objective visible to the training framework.

---

## Source

- **Paper**: [arxiv.org/abs/2604.08423](https://arxiv.org/abs/2604.08423) (preprint, under review)
- **Institution**: Stanford University (Potts and Hashimoto labs)
