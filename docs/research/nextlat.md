# NextLat: Next-Latent Prediction for Compact World Models

> Source: [arXiv:2511.05963](https://arxiv.org/abs/2511.05963) · November 2025

## TL;DR

Standard next-token prediction has no incentive to build compact internal world models — the loss only cares about the next token, not the coherence of the model's internal beliefs. **NextLat** adds a lightweight auxiliary objective: predict the next *latent state*, not just the next token. This injects a recurrent world-model bias into transformers with **no architectural changes**, theoretically provable convergence to belief states, and a bonus: self-speculative decoding that runs up to **3.3× faster**.

---

## The problem with next-token prediction

A standard transformer is trained to maximise P(token_t | token_{1..t-1}). This objective rewards correct next-token predictions but places no pressure on the *internal representation* to be:

- **Compressed**: a compact summary of history sufficient to predict the future
- **Consistent**: transition rules that compose across steps
- **Plannable**: a representation you can roll forward to plan ahead

The model may learn useful internal structure incidentally, but there's no direct incentive. The result: models often lack stable belief states and can't efficiently plan or speculate ahead.

---

## The NextLat auxiliary objective

Alongside the standard next-token loss, NextLat adds:

> **Predict the next latent state** given the current latent state and the next token.

Formally: a small auxiliary head is trained so that `f(h_t, token_{t+1}) ≈ h_{t+1}`, where `h_t` is the transformer's hidden state at step t.

This forces the latent representations to have **consistent transition dynamics** — the model must compress history into a state from which the next state is predictable. The paper proves these latents converge toward **belief states**: the minimal sufficient statistics of history for predicting the future.

No changes to the transformer architecture. No changes to tokenisation or inference graph. Just an auxiliary loss term during training.

---

## Self-speculative decoding

The learned latent dynamics enable a fast inference trick: the model can **speculatively predict future latents** without running full forward passes, then verify only the tokens that actually matter.

This is "variable-length" speculative decoding — the model can decide how far ahead to speculate based on its confidence in the latent trajectory. Result: up to **3.3× wall-clock speedup** in language modelling.

---

## Results

Gains over standard next-token prediction across:

| Domain | Result |
|--------|--------|
| World modeling tasks | Significant accuracy gains |
| Reasoning benchmarks | Significant accuracy gains |
| Planning tasks | Significant accuracy gains |
| Representation compression | Better compressed latents |
| Inference speed | Up to 3.3× via self-speculative decoding |

The method is positioned as orthogonal to architecture improvements — it's a training objective change that stacks on top of any transformer.

---

## Why it matters

The core claim is architectural: current transformers can learn world models, but the training objective doesn't push them to. NextLat is the minimal intervention that makes the objective explicitly require world-model structure, and the bonus speculative decoding speedup is a practical consequence of having those compact, predictable latents.

---

## Source

- **Paper**: [arXiv:2511.05963](https://arxiv.org/abs/2511.05963)
