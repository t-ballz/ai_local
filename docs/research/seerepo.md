# SeeRepo: Visual Dependency Graphs for Code Agents

> Source: [arXiv:2606.14061](https://arxiv.org/abs/2606.14061) · [github.com/cslsolow/SeeRepo](https://github.com/cslsolow/SeeRepo) · 2026

## TL;DR

Coding agents navigate repos as linearized text. SeeRepo adds **visual dependency graph images** alongside text access — AST-derived PNGs showing which files contain, import, invoke, or inherit what. Result on SWE-bench Verified: **−25% input tokens, −26% cost**, accuracy maintained. The catch: vision-*only* is significantly worse than text-only; the gains are hybrid.

---

## The problem

Human developers don't read codebases linearly — they glance at a folder structure, follow an import, check a class hierarchy. Agents do the opposite: retrieve text chunks, construct long context windows, repeat until they've located the relevant file.

This is expensive. Fault localization — the first stage of fixing a bug — requires understanding how the repository fits together globally before zooming in. Text-based agents do this via many sequential tool calls; the global structure only emerges implicitly.

---

## SeeRepo

**Core idea**: augment the agent with a visual representation of the dependency graph at the localization stage, rendered as a PNG using Graphviz. The agent still has text access for reading and editing; the image provides global structural context upfront.

### Graph construction

Built from AST-based static analysis, with four relation types:

| Relation | Meaning |
|----------|---------|
| **contains** | Directory → file, file → class/function |
| **imports** | Module-level import statements |
| **invokes** | Function call relationships |
| **inherits** | Class inheritance |

Subgraphs are centred on the query node and rendered at three levels: **graph** (full DAG), **nested** (hierarchical), **tabular** (compact list). Graph layout performed best in evaluation.

### When to show the image

The agent receives the visual during **fault localization only**. Once the relevant file is identified, repair and validation stages revert to text-only. This avoids flooding the model with images during surgical edits where spatial context is irrelevant.

---

## Results (SWE-bench Verified, 500 instances)

| Setup | Accuracy | Cost vs. baseline |
|-------|----------|------------------|
| Text only (baseline) | 55.0% | 1.0× |
| Vision only | 41.4% | 1.42× |
| **SeeRepo (hybrid)** | **≈55%** | **0.74×** |

Vision-only *hurts*: accuracy drops 13.6 points and cost increases 42% as agents compensate by making more redundant queries. The structural picture alone can't replace reading code.

Hybrid holds accuracy while cutting tokens by 25% — the dependency graph front-loads the structural understanding that would otherwise emerge after many tool calls.

**Best result**: Kimi K2.5 with SeeRepo hybrid → **70.6% Pass@1**, with 3% cost reduction.

---

## Takeaways

1. **Structure as a supplementary modality, not a replacement.** The image provides orientation; the text provides detail. Neither works well without the other.
2. **Localization is the right place to intervene.** The global view pays off at the "where is the bug?" stage; it's noise during "write the fix."
3. **-25% tokens from better navigation.** Not compression — fewer redundant tool calls because the agent has a map before it starts exploring.
4. **Complements existing scaffolds.** SeeRepo wraps around SWE-agent and similar; it's a design dimension (add visual context) not a competing framework.
5. **Relation to FastContext**: FastContext ([wiki page](../models/fastcontext.md)) reduces exploration tokens by specialising a subagent for repo search. SeeRepo reduces them by giving the main agent a visual map. These are complementary: one removes the search problem, the other makes search cheaper.

---

## Source

- **Paper**: [arXiv:2606.14061](https://arxiv.org/abs/2606.14061)
- **Code**: [github.com/cslsolow/SeeRepo](https://github.com/cslsolow/SeeRepo)
