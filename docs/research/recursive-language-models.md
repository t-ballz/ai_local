# Recursive Language Models (RLMs)

> Source: [arxiv.org/abs/2512.24601](https://arxiv.org/abs/2512.24601) · [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm) · Dec 31, 2025 (v3 May 11, 2026)  
> Authors: Alex L. Zhang, Tim Kraska, Omar Khattab — MIT CSAIL

## TL;DR

Instead of extending the context window, RLMs treat the long prompt as an **external Python variable** in a REPL. The model recursively peeks, greps, partitions, and calls itself over subsets of the input — handling prompts "two orders of magnitude beyond model context windows" with **no information loss from summarisation or deletion**. Median improvement on GPT-5: +26% vs compaction, +130% vs CodeAct, +13% vs Claude Code. MIT licence, `pip install rlms`.

---

## The problem

Long-context methods all lose information in some way:

| Method | How it loses information |
|--------|--------------------------|
| Larger context window | "Context rot" — model quality degrades over long inputs even within the window |
| RAG / retrieval | Retrieval misses; chunking destroys cross-chunk dependencies |
| Compaction / summarisation | Irreversible compression; details dropped |
| Agent scrolling | Linear, slow; no structural understanding |

RLMs sidestep this by never forcing the model to fit everything into one forward pass.

---

## How it works

The prompt is stored as a Python variable in a **REPL notebook environment**. The root LM receives the query and a reference to this variable, then generates and executes code to inspect it — launching recursive sub-calls to itself or other LMs as needed.

```python
# The model can do things like:
context = load_variable("user_document")          # 5M token document
section = context[0:10000]                        # peek at structure
results = [sub_rlm(f"find X in: {chunk}")         # map over chunks
           for chunk in partition(context, 50000)]
FINAL(aggregate(results))
```

Four interaction strategies emerged naturally during evaluation:

| Strategy | What it does |
|----------|-------------|
| **Peeking** | Examines initial sections to understand structure before committing |
| **Grepping** | Uses regex/keyword search to narrow the search space |
| **Partition + Map** | Chunks context and runs parallel recursive sub-calls for semantic labelling |
| **Summarisation** | Extracts and condenses targeted subsets (only when needed, not as a lossy default) |

Sub-RLM calls are **native code primitives** — the parent LM decides when to call them and how to aggregate results, enabling arbitrary recursion depth.

---

## Benchmarks

### Median improvement over baselines (GPT-5 host model)

| Baseline | Median improvement |
|----------|--------------------|
| Compaction methods | **+26%** |
| CodeAct with sub-calls | **+130%** |
| Claude Code | **+13%** |

Cost is comparable to existing approaches.

### Per-task breakdown

**OOLONG** — distributional queries over unlabelled 3K–6K-row datasets (context rot test):

| Scale | RLM(GPT-5-mini) vs GPT-5 raw |
|-------|------------------------------|
| 132K tokens | +114% (>33 point absolute gain) |
| 263K tokens | +49% |

**BrowseComp-Plus** — multi-hop retrieval across 100K documents (~5K words each):

- RLM(GPT-5): **100% at 1,000-document scale**
- Only iterative approaches (RLM, ReAct) maintained performance beyond 100 documents

**LoCoDiff** — reconstruct final file state from git diff histories exceeding 75K tokens:

- GPT-5 (vanilla): fails on >90% of histories longer than 75K tokens
- RLM(GPT-5): handles them by implementing programmatic one-shot diff processing

**RULER / Needle-in-haystack**: ~90%+ but these benchmarks don't capture real-world context rot well.

### Open-weight result

RLM-Qwen3-8B outperforms its baseline by **+28.3% on average** — the approach is not limited to frontier models.

---

## Using it

```bash
pip install rlms
```

```python
from rlm import RLM

rlm = RLM(backend="openai", backend_kwargs={"model_name": "gpt-5-nano"})
print(rlm.completion("Your very long prompt here").response)
```

**Supported backends**: OpenAI, Anthropic, OpenRouter, Portkey, local models via vLLM.

**REPL environments**: local Python, IPython, Docker, Modal, E2B (sandboxed cloud).

---

## Limitations

- **Synchronous only** — no async; individual queries can take seconds to minutes
- **No cost/runtime guarantees** — recursive calls can multiply token usage unpredictably
- **No prefix caching** — repeated context re-reads aren't amortised
- Performance degrades more on smaller models at very long contexts

---

## Licence

MIT — [github.com/alexzhang13/rlm](https://github.com/alexzhang13/rlm)
