# SkillHarness: Harnessing Safe Skills for Computer-Use Agents

> Source: [arXiv:2606.20636](https://arxiv.org/abs/2606.20636) · Jun 2026  
> Authors: Yurun Chen, Biao Yi, Keting Yin, Shengyu Zhang

## TL;DR

SkillHarness frames skill development for Computer-Use Agents as a safety-constrained process, using multi-source supervision to identify skill boundaries and context-guided reuse to prevent unsafe invocations. It cuts unsafe skill rates by 57.1% while improving stability under environmental changes like pop-ups and prompt injections.

---

## The problem

Computer-Use Agents learn reusable skills by observing successful trajectories in GUI environments. Existing skill-learning approaches assume static, secure settings — they don't account for adversarial interactions (prompt injections embedded in UI elements) or environmental dynamics (unexpected pop-ups, state changes). A skill learned in a clean environment may trigger unsafe behavior when reused in a hostile or noisy one.

---

## How it works

**Skill boundary identification**: Uses multi-source supervision — combining execution traces, semantic signals, and safety annotations — to determine where a skill begins and ends. This prevents skills from over-generalizing beyond their safe operating context.

**Selective skill reuse**: At inference time, context-guided selection evaluates whether the current environment state is within the learned skill's safe boundary before activating it. Skills that cannot be safely applied fall back to direct step-by-step execution.

The two mechanisms work together: tighter boundaries reduce the surface area for misuse, and contextual gating prevents reuse in unsafe conditions.

---

## Results

| Metric | Improvement |
|---|---|
| Unsafe skill rate | −57.1% vs. baselines |
| Stability under environmental changes | Improved vs. prior skill-learning approaches |

---

## Why it matters for local AI

Computer-use agents running locally face real-world adversarial conditions — websites embed prompt injections, UI states change unpredictably. SkillHarness provides a principled way to build a safe skill library that degrades gracefully rather than being exploited. The multi-source supervision approach is model-agnostic and applicable to any agent that accumulates reusable skills.

---

## Limitations

- Evaluation on standard CUA benchmarks; adversarial test coverage may not reflect all real-world injection vectors
- Skill boundary identification adds overhead compared to naive skill caching
- Safety constraints may occasionally block legitimate skill reuse in benign environments with unusual UI patterns

---

## Source

- **Paper**: [arXiv:2606.20636](https://arxiv.org/abs/2606.20636)
- **Preprint date**: Jun 2026
