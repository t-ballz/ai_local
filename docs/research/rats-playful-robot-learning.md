# RATs: Playful Agentic Robot Learning

> Source: [arXiv:2606.19419](https://arxiv.org/abs/2606.19419) · June 2026  
> Authors: Junyi Zhang, Jiaxin Ge, Hanjun Yoo, Letian Fu, Zihan Yang, et al. (UC Berkeley, UIUC, Google Research)

## TL;DR

Current Code-as-Policy robot agents are task-driven: skills are acquired only after explicit instructions arrive. RATs (Robotics Agent Teams) flips this—an embodied coding agent uses **self-directed play** as a continual skill-learning stage, proposing novel exploratory tasks, executing robot policies, and distilling successful executions into a reusable skill library. At test time, agents retrieve frozen skills to solve new tasks, achieving **+20.6pp and +17pp gains** on downstream robot manipulation benchmarks without fine-tuning.

---

## The problem

Standard agentic robot systems follow a reactive cycle: receive task → generate code → execute → observe → revise. They can write executable policies and learn from feedback, but reusable skills emerge only *after* explicit task instructions. This misses a key opportunity: before any specific task arrives, an agent could **proactively explore** the environment and build a skill library.

This is fundamentally different from human or animal learning—infants and young animals spend significant time in playful, undirected exploration before tackling real-world tasks.

---

## Playful agentic skill acquisition

RATs introduces a three-phase pipeline:

### 1. Play-time skill discovery

An LLM-based agent orchestrates "Robotics Agent Teams" during play:
- **Proposes novel, learnable exploratory tasks** — not arbitrary, but carefully selected to be achievable yet informative
- **Plans and executes robot-code policies** — writes Python code that commands the robot
- **Verifies intermediate progress** — checks whether the task is making progress
- **Diagnoses failures and retries** — provides dense, step-level feedback to refine the approach

All successful executions are distilled into a **persistent code skill library** — a collection of reusable, high-level primitives.

### 2. Skill library freezing

Once play is complete, the learned skills are frozen and indexed for retrieval. No further updates during downstream tasks.

### 3. Test-time skill reuse

When a new task arrives, the agent:
- Retrieves relevant skills from the frozen library (in-context)
- Uses them to compose a solution without fine-tuning the base model
- Solves the downstream task faster and more reliably

---

## Key results

### Benchmark improvements

| Benchmark | Improvement | Baseline |
|-----------|------------|----------|
| LIBERO-PRO | +20.6pp | CaP-Agent0 (no play) |
| MolmoSpaces | +17.0pp | CaP-Agent0 (no play) |
| RoboSuite (skill transfer) | +8.9pp | Agents without skill library |
| Real-world transfer | +8.8pp | Agents without skill library |

### Skill transferability

Learned skills are **zero-shot transferable**: they can be plugged into *other* inference-time Code-as-Policy agents by simply retrieving them into the context. No fine-tuning of the underlying model required. This demonstrates that the skills are genuinely reusable primitives, not artifacts of a particular model or task.

---

## Why it matters

**Proactive learning changes the game for embodied AI.** Rather than waiting for tasks to drive learning, agents can build foundational skills during "off-duty" time. This is more sample-efficient (fewer failures on real downstream tasks) and more aligned with how biological learners actually acquire competence.

The play-learned skills are **model-agnostic** — they work across different Code-as-Policy agents without modification, suggesting the framework captures genuine task structure rather than brittle model-specific patterns.

Real-world transfer improvements (+8.8pp) hint at the practical value: agents prepared by playful pre-exploration transfer better to physical robots, a critical bottleneck in robotics.

---

## Source

- **Paper**: [arXiv:2606.19419](https://arxiv.org/abs/2606.19419)
