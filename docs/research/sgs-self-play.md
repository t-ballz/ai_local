# Scaling Self-Play with Self-Guidance (SGS)

> Source: [arxiv.org/abs/2604.20209](https://arxiv.org/abs/2604.20209) · April 22, 2026  
> Authors: Luke Bailey, Kaiyue Wen, Kefan Dong, Tatsunori Hashimoto, Tengyu Ma (Stanford)

## TL;DR

Self-play training for LLMs breaks down because the model generating synthetic problems learns to "hack" its own reward — producing increasingly bizarre, unsolvable problems that don't help the learner improve. SGS adds a third role, the **Guide**, that scores synthetic problems for relevance and quality before they enter training. With this gating, a **7B model trained for 200 rounds of self-play outperforms a 671B model** (DeepSeek-Prover-V2) at pass@4 on Lean4 theorem proving.

---

## The problem: Conjecturer collapse

Classic asymmetric self-play uses two roles:

- **Solver** — tries to prove theorems (the learner)
- **Conjecturer** — generates new synthetic theorems for the Solver to practice on

The Conjecturer is rewarded when the Solver *fails* to solve its problems (harder = better reward). Over many rounds, the Conjecturer learns to produce degenerate problems — trivially unsolvable or logically incoherent — that maximise its reward without teaching the Solver anything useful. This is called **Conjecturer collapse**.

---

## The fix: Self-Guided Self-Play

SGS adds a **Guide** role using the same LM:

| Role | Does what |
|------|-----------|
| Solver | Attempts to prove problems; improves over self-play rounds |
| Conjecturer | Generates synthetic theorem candidates from the target problem set |
| Guide | Scores each candidate for (a) relevance to unsolved target problems, (b) mathematical elegance and naturalness |

Only high-scoring candidates from the Guide enter the Solver's training set. The Guide's scoring prevents the Conjecturer from collapsing because garbage problems get filtered out regardless of their "difficulty for the Solver" reward.

The key assumption the paper validates: **language models can reliably assess whether a synthetic sub-problem is useful for reaching a target goal** — i.e., the Guide signal is accurate enough to steer training.

---

## Results

Evaluated on **Lean4 formal theorem proving** (miniF2F benchmark):

| System | Params | pass@4 solve rate |
|--------|--------|------------------|
| DeepSeek-Prover-V2 (baseline) | 671B | — (reference) |
| SGS (this work) | **7B** | **beats 671B baseline** |

- SGS surpasses the strongest RL self-play baseline's *asymptotic* solve rate in **< 80 rounds**
- After 200 rounds the 7B model outperforms pass@4 of DeepSeek-Prover-V2 671B
- Scaling laws fitted to cumulative solve-rate curves show continued improvement

---

## Why it matters beyond theorem proving

The bottleneck SGS addresses — running out of high-quality training problems — is not unique to math. Any domain where:

1. Correct answers are verifiable (code execution, formal proofs, structured outputs)
2. A model can generate candidate problems

…is a candidate for this approach. The Guide quality-gate is the key innovation: it turns cheap synthetic generation into usable training signal without human labelling.

This is a step toward models that can **autonomously bootstrap their own training curriculum** on any verifiable task.
