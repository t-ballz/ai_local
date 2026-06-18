# Nothing from Something: Can a Language Model Discover 0?

> Source: [arXiv:2606.17289](https://arxiv.org/abs/2606.17289) · June 2026  
> Authors: Phoebe Zeng, Thomas L. Griffiths, Brenden M. Lake

## TL;DR

Seeing the token `0` is not the same as understanding zero. LLMs routinely encounter `0` embedded in multi-digit numbers (10, 20, 100…) but still **fail to use zero correctly as an arithmetic operand or result** without explicit training examples. Language pretraining helps — it cuts the required examples by ~50% — but produces no zero-shot discovery. Neural networks generalize from learned relational structure, not from logical necessity.

---

## The question

Can a language model discover a mathematical concept it has never seen used correctly, just by reasoning from what it knows?

The researchers chose **zero** as the test case: arguably the simplest mathematical concept that isn't trivially present in pretraining data *in its relational sense*. Models see `0` constantly (in `10`, `20`, `100`, timestamps, IDs…) but rarely as the subject of arithmetic — as an identity element, a boundary, an operand that absorbs or annihilates.

---

## Key findings

### Seeing the token ≠ knowing the concept

A GPT-2 scale model pretrained on text cannot zero-shot generalise to arithmetic involving zero even though `0` appears millions of times in training. The bottleneck is not token frequency — it is whether the **relational role** of zero (identity under addition, annihilator under multiplication, arithmetic boundary) was ever encoded.

### How many examples does it need?

With no pretraining: hundreds to thousands of zero-containing arithmetic examples required to generalise.

With language pretraining: tens to hundreds of examples — roughly a **50% reduction**.

Language pretraining scaffolds mathematical discovery: the linguistic structure around number concepts gives the model footholds that shorten the path, but it does not close the gap to zero-shot.

### Generalization is relational, not logical

The core conclusion: neural networks do not generalise a concept because it is *logically entailed* by what they know. They generalise when the required **relational structure** — zero as identity, operand, result, boundary — is present in training data or can be assembled from connected existing structures.

"Nothing from something" is a riff on the usual direction: these models cannot produce structured understanding of zero from unstructured exposure.

---

## Why it matters for LLM training

- **Data curation over data volume**: high token frequency of a symbol does not substitute for examples that demonstrate its *roles*. A model that sees `0` a billion times in phone numbers learns nothing about arithmetic zero.
- **Scaffolding works, but incompletely**: language pretraining meaningfully reduces the sample complexity of mathematical concept learning — but targeted examples remain necessary.
- **Benchmark design**: tasks that assume a concept is "obviously in training data" because the token is common may be measuring something else entirely.

---

## Limitations

- Evaluated on GPT-2 scale models — larger models may close the gap somewhat via in-context assembly across more training-data connections.
- Simple arithmetic setting — more complex concepts may show different dynamics.
- Zero is an unusually clean case (the relational gap is easy to construct); other concepts may be harder to isolate this cleanly.

---

## Source

- **Paper**: [arXiv:2606.17289](https://arxiv.org/abs/2606.17289)
