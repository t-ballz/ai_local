# ENPIRE: Agentic Robot Policy Self-Improvement in the Real World

> Source: [arXiv:2606.19980](https://arxiv.org/abs/2606.19980) · June 2026  
> Authors: Wenli Xiao, Jia Xie, Tonghe Zhang, Haotian Lin, Letian "Max" Fu, Haoru Xue, Jalen Lu, Yi Yang, Cunxi Dai, Zi Wang, Jimmy Wu, Guanzhi Wang, S. Shankar Sastry, Ken Goldberg, Linxi "Jim" Fan, Yuke Zhu, Guanya Shi

## TL;DR

ENPIRE is a multi-agent framework where AI coding agents autonomously improve robot manipulation policies by programming, testing, and refining algorithms through repeated real-world trials. A decentralized team of specialized agents handles environment setup, policy optimization, and rollout coordination. The system achieves **99% success rates on dexterous manipulation tasks** and **3.75× faster convergence** with 8 parallel robots compared to single-robot baselines.

---

## The problem

Robot manipulation tasks require precise, task-specific policies that are expensive to hand-engineer. Traditional methods rely on:

- Manual policy design by engineers
- Slow, centralized optimization loops
- Limited scalability across robot fleets

Real-world robot learning needs to be **autonomous, scalable, and efficient** — but humans currently bottleneck policy improvement through manual intervention.

---

## Architecture: Decentralized multi-agent teams

ENPIRE decomposes policy self-improvement into four specialized agent roles running asynchronously:

### Environment Setup Agents
- Manage scene reset and state verification
- Define task-specific reward functions
- Enforce safety constraints and episode termination conditions

### Policy Optimization Agents
- Analyze failure modes from robot rollouts
- Generate code modifications to improve algorithms
- Use multiple optimization strategies: behavioral cloning (BC), reinforcement learning (RL), and domain-specific heuristics

### Rollout Module
- Execute policies on parallel robot hardware
- Collect trajectory data and outcome labels
- Report successes and failure modes back to optimization agents

### Evolution Module
- Synthesize failure reports from robot trials
- Direct optimization agents to specific failure types
- Iterate policy refinement across learning cycles

**Key insight:** By decentralizing control and enabling asynchronous updates, multiple agents can work on different aspects of the problem simultaneously without blocking on centralized decision-making.

---

## Results

### Task performance

Evaluated on complex dexterous manipulation tasks:

| Task | Success Rate |
|------|---------------|
| Pin insertion | 99% |
| Pushing | 99% |
| Zip-tie cutting | 99% |

### Scaling efficiency

With **8 parallel robots**:
- **3.75× faster convergence** to high-performance policies vs. single-robot baseline
- Near-linear speedup with additional robots (limited only by shared environment reset overhead)
- Decentralized execution reduces coordinator bottlenecks

### Real-world robustness

- Policies transfer successfully across different robot instances
- System recovers from hardware failures and unexpected environmental variations
- Learned skills generalize to unseen object configurations

---

## Why it matters

- **Autonomous policy improvement**: Removes humans from the optimization loop entirely; agents handle problem decomposition, experimentation, and iteration
- **Real-world scalability**: Demonstrates that robot fleets can improve themselves in parallel without centralized orchestration
- **High-success-rate learning**: 99% dexterous task success shows the system reliably finds robust policies
- **Multi-agent system design**: The decentralized architecture is a blueprint for scaling autonomous learning across heterogeneous robot teams
- **Practical robot learning**: Transforms manipulation learning from a supervised/reward-design problem into a controllable, closed-loop optimization procedure

---

## Source

- **Paper**: [arXiv:2606.19980](https://arxiv.org/abs/2606.19980)
