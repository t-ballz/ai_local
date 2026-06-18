# Is It Agentic Enough? Benchmarking Open Models on Your Own Tooling

> Source: [Hugging Face Blog](https://huggingface.co/blog/is-it-agentic-enough) · June 2026

## TL;DR

A harness for evaluating open-weight models as coding agents on the `transformers` library reveals a key insight: **improvements for large models can actively harm smaller ones**. Qwen3-14B goes from 100% to 0% on a task when CLI documentation is added — because it misreads the CLI as a Python-callable tool. Model size, not just capability, changes how models interpret affordances.

---

## What's being measured

Not just correctness — but *effort*: token consumption, latency, error rates, and behavioral patterns. The research frames evaluation as: "not just whether the agent got it right, but how much work it took to get there."

---

## Models tested

| Category | Models |
|----------|--------|
| Large | Kimi-K2.6, GLM-5.1, MiniMax-M2.7 |
| Small | Qwen3-4B, Qwen3-14B |

Large models typically succeed; the metrics shift to efficiency. Small models are measured on success rate first.

---

## Tasks and conditions

Three `transformers` library tasks:
- Text classification
- Image captioning
- Audio transcription

Three tooling tiers per model:

| Tier | What's available |
|------|-----------------|
| `bare` | Standard pip install |
| `clone` | Full source repository |
| `skill` | Curated CLI documentation and examples |

---

## Key finding: docs help large models, break small ones

Adding CLI documentation (the `skill` tier):
- **Large models**: Improved — adoption rate 55.3% when docs available
- **Qwen3-14B**: 100% accuracy (with source) → **0%** (with skill docs)

The failure mode: Qwen3-14B treated the CLI command as a Python-callable object rather than a shell-executable. The documentation introduced ambiguity the smaller model couldn't resolve.

**Implication**: API/tool design for agents must be tested at the model scale you'll deploy. An interface optimised for GPT-4 class models may actively mislead 7B–14B models.

---

## The Markers framework

A behavioural tracking system that logs named patterns across runs:

- `cli` marker: did the agent use the CLI directly, or write Python code instead?
- `pipeline` marker: did the agent use `pipeline()` API vs lower-level calls?

This surfaces *how* models use tools, not just whether they succeed — useful for debugging why agents underperform with a particular interface.

---

## Takeaways for local deployment

1. **Don't benchmark only at target scale** — test what happens a tier or two smaller.
2. **CLI docs can backfire** — agents that can't parse shell vs Python distinctions will fail.
3. **Measure token cost, not just accuracy** — a 3× token overhead on success matters at inference time.
4. **Build markers into your own evals** — track *how* your agent uses tools, not just outcomes.

---

## Source

- **Blog**: [Is it agentic enough? Benchmarking open models on your own tooling](https://huggingface.co/blog/is-it-agentic-enough)
