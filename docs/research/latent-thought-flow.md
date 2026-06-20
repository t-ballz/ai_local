# Latent Thought Flow: Efficient Latent Reasoning in LLMs

> Source: [arXiv:2606.16222](https://arxiv.org/abs/2606.16222) · June 2026  
> Authors: Xiandong Zou, Jing Huang, Jianshu Li, Pan Zhou

## TL;DR

Latent Thought Flow (LTF) moves reasoning from discrete token sequences into continuous latent space, modeled as variable-length trajectories through a learned generative flow. A continuous GFlowNet learns to allocate probability to reasoning paths that are both correct and computationally cheap, enabling adaptive compute (early exit on easy problems, more reasoning on hard ones). Result: +9.5% accuracy, −27.2% reasoning length reduction over latent baselines.

---

## The problem

**Explicit Chain-of-Thought reasoning is expensive**: each thought must be decoded into tokens, creating massive inference overhead. Latent reasoning (reasoning in hidden space) avoids tokenization but treats it as a fixed-length or simple optimization process.

**Current latent approaches lack efficiency signals**: they don't distinguish between cheap correct reasoning and expensive correct reasoning, nor do they adapt compute to problem difficulty.

---

## Latent Thought Flow approach

### Reasoning as trajectories in latent space

LTF models reasoning as **variable-length paths** through a continuous latent space. Each trajectory is a sequence of latent states leading to a final answer, with variable trajectory length reflecting adaptive compute.

### Continuous GFlowNet for trajectory learning

A continuous **Generative Flow Network (GFlowNet)** learns a distribution over valid reasoning trajectories. Unlike standard diffusion or VAE approaches:

- **Stochastic transitions** with learnable parametric flow allow smooth navigation through latent space
- **Entropy-Weighted Subtrajectory Balance objective** ensures that partial trajectories and full trajectories are both weighted appropriately — longer reasoning only pays off if it improves correctness
- **Reference-prior regularizer** grounds trajectories toward high-value states, preventing collapse into cheap-but-wrong solutions

### Adaptive compute

The GFlowNet naturally learns to:
1. **Short-circuit easy problems**: simple queries terminate early with high probability
2. **Allocate depth to hard problems**: complex reasoning paths receive higher probability mass on difficult instances
3. **Balance accuracy and cost**: the flow balances "reward" (correct answer) against path length, trading off accuracy gains against computational budget

---

## Key results

**Benchmark**: standard reasoning tasks (GSM8K-style math, logic, QA)

| Metric | Result |
|--------|--------|
| Accuracy gain | +9.5% vs. latent baselines |
| Reasoning length reduction | −27.2% (avg trajectory shorter) |
| Adaptive compute | Early exit observed on easy instances |

---

## Why it matters

- **Inference efficiency**: eliminates tokenization overhead of CoT while retaining reasoning depth
- **Interpretability signal**: latent trajectories are shorter and more selective than CoT token sequences, potentially easier to analyze
- **Adaptive by design**: the model naturally learns to spend compute only where it matters, without explicit length penalties or auxiliary losses
- **Scalable**: works with any base LLM architecture by replacing or augmenting the reasoning module

---

## Source

- **Paper**: [arXiv:2606.16222](https://arxiv.org/abs/2606.16222)
