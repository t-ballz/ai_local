# Environment-Aware IR: Retriever-Adaptive Queries

> Source: [arXiv:2606.16817](https://arxiv.org/abs/2606.16817) · June 2026  
> Authors: Ruifeng Yuan, Chaohao Yuan, David Dai, Yu Rong, Hong Cheng, Hou Pong Chan, Chenghao Xiao

## TL;DR

Different retrievers require fundamentally different query formulation strategies. This work shows that LLMs can learn retriever-specific optimal query styles via reinforcement learning (RL) — e.g., Contriever prefers descriptive queries while Qwen3-Embedding prefers question-like formats. Strategies don't transfer across retrievers. A branching-based rollout technique improves training stability.

---

## The problem

Retrieval-augmented generation (RAG) systems rely on query formulation to retrieve relevant documents, yet current approaches treat query writing as retriever-agnostic. In reality, different retrievers have different embedding spaces, training objectives, and optimal input styles. An LLM trained to write queries for one retriever may perform poorly with another, but this critical mismatch has been largely overlooked.

The core challenge: how can we enable LLMs to dynamically adapt their query formulation to the specific retriever in use?

---

## Approach: RL-based retriever-aware query adaptation

The work presents the first systematic analysis of how LLMs learn retriever-specific query strategies via RL:

1. **Baseline**: Standard query formulation (e.g., rephrasing, expanding, simplifying the original question)
2. **RL training**: An LLM learns a policy to rewrite queries, optimizing for retrieval performance on a specific retriever
3. **Reward signal**: Retrieval ranking metrics (e.g., nDCG@k) based on the target retriever's output
4. **Key innovation**: Branching-based rollout technique — instead of single-trajectory rollouts, the policy explores multiple query rewrites per step and aggregates their feedback. This improves training stability over multi-step retrieval trajectories.

Additional findings:
- Incorporating **retriever-specific human guidance** further improves performance
- Performance scales with model size
- Results suggest deeper architectural fit between query style and retriever embedding space

---

## Key results

**Different retrievers, different optimal styles:**
- **Contriever**: Prefers descriptive, context-rich queries
- **Qwen3-Embedding**: Prefers concise, question-like formats
- Other retrievers show additional style preferences

**Lack of transfer:**
Strategies learned for one retriever are ineffective for another. An LLM trained to optimize queries for Contriever performs poorly with Qwen3-Embedding, even though both are dense retrievers. This suggests that optimal query formulation is tightly coupled to retriever-specific characteristics.

**Branching-based rollout:**
Multi-step retrieval trajectories are unstable to train. Branching rollouts—exploring multiple query candidates and their downstream effects—improve training signal and stability.

**Human guidance helps:**
Providing retriever-specific examples or guidance during RL training boosts final performance, suggesting that LLMs can learn to internalize retriever preferences.

---

## Why it matters

This work challenges the assumption that query formulation is a universal skill. In practice:

- **Better RAG systems**: RAG applications can now optimize query writing for their specific retriever, rather than hoping a generic strategy will work.
- **Quantifies the mismatch**: The paper provides empirical evidence that retriever selection and query strategy are co-dependent design choices.
- **Enables system-aware LLMs**: LLMs in RAG systems can learn to "understand" and adapt to their environment — a step toward more context-aware and efficient RAG architectures.

This is especially relevant as retrieval systems proliferate (different embedding models, proprietary retrievers, domain-specific indices). A truly effective RAG system must be environment-aware.

---

## Source

- **Paper**: [arXiv:2606.16817](https://arxiv.org/abs/2606.16817)
- **Code**: [GitHub: LCO-Embedding/Envs-aware-Information-Retrieval](https://github.com/LCO-Embedding/Envs-aware-Information-Retrieval)
