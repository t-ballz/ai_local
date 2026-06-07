# Harness-1

> Source: [arXiv 2606.02373](https://arxiv.org/abs/2606.02373) · [HuggingFace: pat-jj/harness-1](https://huggingface.co/pat-jj/harness-1) · [GitHub: pat-jj/harness-1](https://github.com/pat-jj/harness-1)

## TL;DR

A **20B open-weight search agent** trained with reinforcement learning inside a stateful search harness. Achieves 73% average evidence recall across 8 retrieval benchmarks, matching much larger frontier models at a fraction of their cost. Released June 2026 by Patrick Jiang (independent researcher).

---

## What it does

Harness-1 performs **long-horizon web search**: multi-step query planning, evidence retrieval, verification, and answer synthesis.

### Key insight: state externalization

Most search agents are trained as policies over growing transcripts — the model must simultaneously make semantic decisions *and* track candidate lists, evidence, verification state, and search history. This wastes RL capacity on recoverable bookkeeping.

Harness-1 offloads all state management to an external harness:

| Maintained by harness | Decided by model |
|-----------------------|-----------------|
| Candidate pool | Which queries to run |
| Curated evidence + links | Which evidence to trust |
| Verification records | When to stop searching |
| Budget-aware context rendering | How to synthesize the answer |
| Search history | — |

The policy focuses purely on semantic decisions; the environment handles bookkeeping.

---

## Specs

| Property | Value |
|----------|-------|
| Params | ~21B |
| Base model | openai/gpt-oss-20b (BF16 safetensors) |
| Format | HuggingFace safetensors |
| VRAM (BF16) | ~42 GB |

---

## Benchmarks

Evaluated across 8 retrieval benchmarks (web, finance, patents, multi-hop QA):

| Metric | Score |
|--------|-------|
| Average evidence recall | 0.730 (73%) |
| vs. next best open search agent | +11.4 points |
| vs. frontier model searchers | Competitive with Opus-4.6; outperforms GPT-5.4 on search |

---

## Running locally

At ~42 GB BF16, Harness-1 requires a multi-GPU or high-VRAM setup for full local inference. Practical options:

- vLLM or llama.cpp with multi-GPU tensor parallelism
- The harness framework is model-agnostic — it can wrap a lighter local model for lower-cost search pipelines

---

## Source & licence

- **Paper**: [arXiv 2606.02373](https://arxiv.org/abs/2606.02373)
- **Model**: [pat-jj/harness-1](https://huggingface.co/pat-jj/harness-1)
- **Code / harness**: [github.com/pat-jj/harness-1](https://github.com/pat-jj/harness-1)
