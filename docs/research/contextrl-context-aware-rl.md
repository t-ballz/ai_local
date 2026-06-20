# ContextRL: Context-Aware RL for Agentic and Multimodal LLMs

> Source: [arXiv:2606.17053](https://arxiv.org/abs/2606.17053) · June 2026  
> Authors: Peiyang Xu, Bangzheng Li, Sijia Liu, Karthik R. Narasimhan, Pramod Viswanath, Prateek Mittal, Xingyu Fu

## TL;DR

ContextRL adds a contrastive context-selection objective to standard policy gradient methods (e.g., GRPO) to help models distinguish supporting from confounding context. Instead of supervising only the final answer, models are rewarded for selecting between two highly similar contexts — one supporting the query–answer pair, one not — enabling fine-grained grounding. Achieves +2.2% gains on long-horizon reasoning (5 benchmarks) and +1.8% on visual QA (12 benchmarks).

---

## The problem

LLMs often fail when success requires identifying a small but decisive piece of evidence within complex or long contexts: a single line in a tool trace, a subtle detail in an image, or a critical fact buried in documentation. Standard RL training (e.g., GRPO) supervises the final answer but provides no explicit signal to ground reasoning on the *right* parts of the input.

This leads to:
- **Spurious correlations**: models learn to output correct answers without grounding on supporting evidence
- **Brittleness in long-horizon tasks**: agentic LLMs fail on SWE-bench style problems where a single tool output matters
- **Weak multimodal grounding**: visual reasoning models miss subtle details in images

---

## Context-Selection Objective

ContextRL introduces an auxiliary objective that trains models to select the context that supports a query–answer pair from a pair of highly similar contexts.

### Training setup

1. **Query, answer, two contexts**: model sees (query, correct_answer, context_A, context_B)
2. **Contrastive design**: context_A supports the query–answer pair; context_B is a confounding or irrelevant variant
3. **Reward signal**: model is rewarded for selecting the supporting context
4. **Combined loss**: context-selection objective runs alongside standard policy gradient (GRPO), allowing models to learn grounding as an auxiliary task

This indirect supervision avoids hand-labeling which input features matter — instead the model learns to distinguish supporting from confounding evidence through contrast.

---

## Contrastive Data Construction

### Agentic RL (Coding)

**Domain**: Software engineering tasks (SWE-bench style)  
**Context**: tool execution trajectories  
**Dataset size**: 1k context pairs  
**Method**: Condition filtering — automatically select trajectories that lead to the same answer via different intermediate paths, then filter one to remove critical information

### Multimodal RL (Visual Reasoning)

**Domain**: Visual question answering  
**Dataset size**: 7k context pairs  
**Methods**:
- **Generative editing**: modify images to remove or obscure key details
- **Similarity search**: pair images with high visual similarity but different answers

---

## Key Results

### Agentic RL (5 long-horizon benchmarks)
- **+2.2% average improvement** over GRPO baseline
- Strongest gains on multi-step tasks requiring fine-grained state tracking

### Multimodal RL (12 diverse VQA benchmarks)
- **+1.8% average improvement** over GRPO baseline
- Consistent gains across diverse visual reasoning tasks

### Ablation: Data vs. Objective

Baselines that repurpose contrastive contexts as standard query–context–answer examples (no contrastive selection):
- **Provide little to no improvement** over GRPO
- Confirms that gains come from the contrastive selection objective, not the data alone

---

## Why it matters

- **Applicable to both agentic and multimodal LLMs** — a single auxiliary objective works across domains
- **Works with standard RL infrastructure** — integrates cleanly with GRPO and other policy gradient methods
- **Interpretable learning signal** — by rewarding context selection, the model explicitly grounds reasoning on supporting evidence
- **Modest data requirement** — 1k–7k contrastive pairs sufficient to achieve consistent gains
- **Opens the door to fine-grained RL** — suggests auxiliary objectives targeting specific reasoning skills can improve long-horizon and multimodal performance
- **No inference cost** — the contrastive objective is training-only; inference runs standard GRPO

---

## Source

- **Paper**: [arXiv:2606.17053](https://arxiv.org/abs/2606.17053)
