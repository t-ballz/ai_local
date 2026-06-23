# SePO: Self-Evolving Prompt Agent for System Prompt Optimization

> Source: [arXiv:2606.04465](https://arxiv.org/abs/2606.04465) · June 2026  
> Authors: Wangcheng Tao, Han Wu, Weng-Fai Wong

## TL;DR

A meta-optimizer that evolves its own system prompt in a closed self-referential loop. Previous prompt optimizers (TextGrad, MetaSPO) had their own instructions hand-tuned by engineers. SePO treats the prompt agent's prompt as an optimization target and searches for better versions using the same evolutionary search it applies to task agents. Result: **4.49pp average accuracy improvement** across five domains; cheaper than TextGrad on many tasks; discovers defensive principles autonomously (avoid reducing reasoning depth, avoid overfitting test cases).

---

## The problem

Prompt optimization tools automate the search for better task instructions, but they themselves rely on hand-crafted meta-prompts. An engineer writes "you are an optimizer; generate candidate prompts by..." and that meta-prompt is frozen in place. This creates an asymmetry:
- Task agents can evolve their prompts
- The prompt agent cannot evolve its own

This asymmetry means the prompt optimizer is suboptimal by design. What if the prompt agent's own instructions were treated as another optimization target?

---

## How it works

### Self-referential evolutionary search

SePO evolves a prompt agent's system prompt using the same evolutionary loop it applies to task agents:

1. **Generate** — sample candidate meta-prompts from an archive of high-performing versions
2. **Evaluate** — run each candidate meta-prompt; measure how well it optimizes task agents
3. **Archive** — retain the best N meta-prompts (e.g., top 10)
4. **Iterate** — use the archive to generate the next batch of candidates

The loop is closed: better meta-prompts produce better optimizations, which improve the evaluation metric, which drives meta-prompt selection.

### Two-stage training

**Stage 1: Pretraining** (Cost: $37.14 total)
- Train on a multi-task pool (AIME'25, ARC-AGI-1, Sudoku, GPQA, MBPP)
- The prompt agent learns what makes a good optimizer, not just good prompts
- Cost amortized across tasks: ~$7.43/task

**Stage 2: Per-task fine-tuning** (Cost: $2.41–$15.51 per task)
- Continue evolution on the specific target task
- Refines the meta-prompt for that task's characteristics

**Cost comparison:**
- TextGrad: $14.75–$26.52 per task
- MetaSPO: varies (no fixed baseline)
- SePO: $2.41–$15.51 (cheaper in many cases due to amortized pretraining)

### What the agent discovers

The evolved meta-prompt self-discovers defensive principles:
- **Avoid reducing reasoning depth** — don't strip intermediate steps from prompts
- **Avoid overfitting test cases** — don't optimize for memorized examples
- **Avoid overwriting existing behavior** — preserve working instructions when making edits

These principles emerge from the optimization objective, not from hand-coded guidance. The agent learns what makes a robust optimizer.

---

## Results

**Benchmarks (5 domains):**

| Task | Manual-CoT | SePO | Gain |
|---|---|---|---|
| AIME'25 | 29.33% | 33.51% | +4.18pp |
| ARC-AGI-1 | 37.30% | 43.39% | +6.09pp |
| Sudoku | 96.95% | 99.90% | +2.95pp |
| GPQA | 72.54% | 76.26% | +3.72pp |
| MBPP | 63.42% | 70.42% | +7.00pp |
| **Average** | **71.89%** | **76.38%** | **+4.49pp** |

**Comparison to prior methods:**

- **TextGrad**: Failed to beat Manual-CoT on 4 of 5 tasks
- **MetaSPO**: Failed to beat Manual-CoT on 3 of 5 tasks
- **SePO**: Beat Manual-CoT on all 5 tasks

**Generalization:** Sudoku was never seen during pretraining, yet SePO achieved 99.90% accuracy—demonstrating that the learned optimization skill transfers to unseen task distributions.

---

## Why it matters

1. **Prompt engineering is becoming a learnable skill, not a craft.** The system learns *how to optimize prompts*, not just *which prompts work*. This skill generalizes to new tasks.

2. **Self-referential loops can be stable and beneficial.** A common intuition is that a system optimizing itself risks instability or degenerate solutions. SePO shows that evolutionary search with archival can maintain quality while enabling self-improvement.

3. **Pretraining amortizes the cost.** A single $37.14 pretraining run reduces per-task optimization costs to $2–$15, making large-scale prompt optimization practical.

4. **Autonomy scales further than hand-tuning.** Prior methods required human engineers to write meta-prompts. SePO requires only an evaluation metric—the agent discovers the optimizer itself.

5. **Open-weight models benefit equally.** The method is agnostic to model architecture or API access; it works anywhere you can measure task performance.

---

## Limitations and notes

- **Evaluation metric dependency**: The evolved optimizer optimizes for whatever metric you provide. If the metric is misaligned with true task quality, the evolved meta-prompt will be too.

- **Computational cost**: Evolutionary search requires multiple passes over the evaluation set. Pretraining is amortized, but per-task fine-tuning still requires dozens of candidate evaluations.

- **Archive size hyperparameter**: The quality and diversity of the evolved meta-prompts depend on archive size and mutation strategy. No principled way to set these is described.

- **Comparison fairness**: TextGrad and MetaSPO may have been suboptimally configured; a fair comparison would require tuning all methods' hyperparameters on the same validation set.

---

## Related work

- [FAPO: Fully Autonomous Prompt Optimization of Multi-Step LLM Pipelines](fapo-autonomous-prompt-optimization.md) — optimizes multi-step pipelines by diagnosing bottlenecks at each step
- TextGrad (LLM-based gradient descent for prompt optimization)
- MetaSPO (Meta-learning for system prompt optimization)

---

## Source

- **Paper**: [arXiv:2606.04465](https://arxiv.org/abs/2606.04465)
- **Code**: [GitHub: taowangcheng/SePO](https://github.com/taowangcheng/SePO)
- **Authors**: Wangcheng Tao, Han Wu, Weng-Fai Wong
- **License**: CC BY 4.0
