# S2L-PO: Smaller Models as Explorers in GRPO

> Source: [arXiv:2605.30789](https://arxiv.org/abs/2605.30789) · Tsinghua / Qwen / InternLM · 2025

## TL;DR

GRPO needs diverse rollouts to train well, but high-temperature sampling produces incoherent exploration. S2L-PO (Small-to-Large Policy Optimisation) fixes this by using a **frozen smaller model from the same family** as the rollout generator. Smaller models produce structurally diverse yet logically coherent trajectories — natural exploration via capacity compression, not noise injection. Result: **+8.8% on AIME24** when using a 1.7B model to guide training of an 8B model.

---

## The problem with GRPO exploration

Group Relative Policy Optimisation (GRPO) trains a model by generating multiple rollouts per problem, scoring them, and updating toward the better ones. The quality of training depends heavily on diversity in those rollouts — you need different attempts, not the same answer repeated with slight wording variations.

The standard fix is high temperature. But temperature adds **token-level noise**: each decoding step is independently perturbed. The result is diverse in a bad way — logically incoherent trajectories that can't solve the problem even when they accidentally diverge into an interesting direction.

---

## The S2L-PO insight

When a large model is compressed into a smaller one from the same family, the capacity reduction doesn't just remove knowledge uniformly — it induces a **time-invariant perturbation** across the entire reasoning trajectory. The smaller model reasons *differently* at a structural level, not randomly at each step.

This is **policy-level diversity**: the entire trajectory diverges from what the large model would produce, but it stays internally coherent. The small model genuinely tries a different approach.

```
Large model rollout:    A → B → C → D (correct)
High-temp rollout:      A → B' → C → D (token noise, still same path)
Small model rollout:    A → X → Y → D (different strategy, still coherent)
```

---

## How S2L-PO works

1. **Frozen small model** from the same family (e.g. 1.7B sibling of an 8B target) generates rollouts — not fine-tuned, just used as-is
2. **Progressive annealing**: early training mixes small-model rollouts heavily; later phases shift toward on-policy large-model rollouts
3. **No changes to GRPO itself** — only the rollout generation step changes; all scoring and update logic remains identical

The annealing schedule prevents distribution mismatch: starting with too much on-policy data before the model has learned anything useful is wasteful; starting with only small-model data and never transitioning creates a distribution gap.

---

## Results

| Setting | Metric | Gain |
|---------|--------|------|
| 1.7B → 8B on AIME24 | Pass rate | +8.8% |
| Average across settings | Various math | ~9% |
| Out-of-domain (CommonsenseQA) | Accuracy | Positive transfer |
| Training convergence | Effective steps | Faster |

Compute: small-model rollouts are cheap (1.7B vs 8B), and the cost can be amortised across training runs.

---

## Why this matters for training practitioners

| Conventional approach | S2L-PO |
|----------------------|--------|
| High temperature for diversity | Frozen small model |
| Token-level noise | Policy-level structural diversity |
| Incoherent trajectories | Coherent alternative strategies |
| Same compute | Lower rollout cost |

The key reframe: **exploration is a property of the policy, not the sampling parameters.** Smaller models from the same family are already diverse by construction — compression forces them to develop different strategies.

---

## Limitations

- Requires having a smaller model from the same family available
- Progressive annealing schedule requires tuning
- Results focused on mathematical reasoning; transfer to other domains less characterised

---

## Source

- **Paper**: [arXiv:2605.30789](https://arxiv.org/abs/2605.30789)
- **Institution**: Tsinghua University, Qwen team, InternLM team
