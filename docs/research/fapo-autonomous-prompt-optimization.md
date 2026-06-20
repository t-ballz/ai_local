# FAPO: Fully Autonomous Prompt Optimization of Multi-Step LLM Pipelines

> Source: [arXiv:2606.19605](https://arxiv.org/abs/2606.19605) · June 2026  
> Authors: Paul Kassianik, Baturay Saglam, Huaibo Zhao, Blaine Nelson, Supriti Vijay, Aman Priyanshu, Amin Karbasi

## TL;DR

Multi-step LLM pipelines fail due to interactions among retrieval, reasoning, and formatting steps—not always because the model is weak. FAPO is an autonomous framework that evaluates pipeline outputs, diagnoses bottlenecks at each intermediate step, and iteratively optimizes them. It prioritizes **prompt refinements first**, then escalates to structural pipeline changes only when evidence suggests the bottleneck is architectural. Results: **+14.1pp average, +33.8pp when structural changes needed** across 6 benchmarks; tested on Foundation-Sec-8B.

---

## The problem

Multi-step LLM pipelines rely on chains of operations: retrieve context, reason over it, format output. When a pipeline fails, the cause is opaque:
- Is the retriever missing relevant information?
- Is the reasoner failing to synthesize?
- Is the formatter mangling valid output?
- Are these failures independent or coupled?

Manual debugging is slow. Automated optimization typically treats the pipeline as a black box and tweaks the final prompt globally. But a global prompt change can't fix a retrieval failure or a malformed reasoning chain.

---

## Method: iterative diagnosis and constrained optimization

FAPO operates in cycles:

1. **Evaluate** — run the full pipeline on a held-out test set; measure end-to-end performance
2. **Diagnose** — examine intermediate outputs (post-retrieval, post-reasoning) to pinpoint which step(s) are failing
3. **Propose constrained edits** — suggest targeted modifications: rephrasing a retrieval prompt, adding reasoning scaffolding, or (only if diagnosis demands it) restructuring the pipeline
4. **Test in isolation** — validate each proposed change against performance metrics
5. **Commit or backtrack** — apply successful edits; retain others for future combinations

### Prioritization: prompts before structure

The framework embodies a key insight: **most multi-step failures are prompt failures, not architectural failures.**

- Start by optimizing prompts at each step (retrieval prompt, reasoning prompt, formatting prompt)
- Only escalate to structural changes (add a new step, remove a step, change the DAG) when prompt optimization plateaus and diagnosis shows the bottleneck is irreducible without restructuring

This is not dogma—it's data-driven. If diagnosis shows retrieval is missing signals that no prompt can fix without changing how retrieval is invoked, structure changes become justified.

### Implementation on open-weight models

FAPO is demonstrated on **Foundation-Sec-8B**, an open-weight security-focused LLM, with human-in-the-loop validation on intermediate proposals. The framework is generalizable: any LLM capable of multi-step reasoning can be used.

---

## Key results

| Benchmark/Task | Performance Gain |
|---|---|
| Average across 6 benchmarks | **+14.1pp** (prompt optimizations only) |
| When structural changes invoked | **+33.8pp** (combined prompt + structure) |
| CVE classification (Foundation-Sec-8B) | +2.0pp to +7.1pp depending on model variant |
| Outperforms GEPA baseline | 18 of 18 model-benchmark scenarios improve |

**Inverse scaling pattern:** gains are largest on harder tasks and weaker baseline prompts, where the interaction structure is most critical.

---

## Why it matters

1. **Pipelines are programs, not black boxes.** When they fail, we need to debug them like code: trace execution, isolate the failure site, apply targeted fixes.

2. **Autonomous pipeline optimization is practical and scalable.** Manual debugging doesn't scale to dozens of custom pipelines in production. FAPO makes it feasible to keep pipelines self-improving.

3. **Prompts are often the bottleneck, not the model.** A 8B model with a well-optimized multi-step pipeline can outperform a larger model with a generic one. This matters for cost and latency.

4. **Structure should be decided by evidence, not intuition.** By using diagnostic traces, FAPO avoids premature architectural refactoring while not leaving gains on the table when structure *is* the issue.

5. **Open-weight models are viable for complex workflows.** Demonstration on Foundation-Sec-8B shows that autonomous optimization isn't limited to proprietary APIs; it works on downloadable, deployable models.

---

## Source

- **Paper**: [arXiv:2606.19605](https://arxiv.org/abs/2606.19605)
- **Authors**: Paul Kassianik, Baturay Saglam, Huaibo Zhao, Blaine Nelson, Supriti Vijay, Aman Priyanshu, Amin Karbasi
