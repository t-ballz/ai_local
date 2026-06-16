# HarnessX: Evolvable Agent Harnesses

> Source: [arXiv:2606.14249](https://arxiv.org/abs/2606.14249) · Anthropic · 2026  
> Code: planned open-source release

## TL;DR

Agent harnesses (prompts + tools + memory + control flow) are usually hand-crafted once and left static. HarnessX treats the harness itself as a first-class optimisation target: a runtime artifact that automatically adapts from execution traces, then co-evolves with the model being trained. Average gain: **+14.5% across 15 model–benchmark configs**, with another +4-5% when harness evolution is coupled with model training.

---

## The problem

Building a good agent harness is expensive, brittle, and non-transferable:
- Hand-crafted scaffolds degrade as models improve (or don't improve to match the harness)
- Execution traces are discarded rather than converted into harness improvements
- Model RL and harness tuning are done separately, leaving a ceiling neither can break alone

HarnessX calls these the *scaffolding ceiling* (harness limits a better model) and the *training-signal ceiling* (model RL is limited by a static harness).

---

## Architecture: three layers

### Layer 1 — Harness Composition

Harnesses are decomposed into **9 behavioral dimensions**: model selection, context assembly, memory, tools, execution environment, evaluation, control/safety, observability, and training bridge.

Each dimension is implemented as a typed **processor** with lifecycle hooks. Processors compose via a substitution algebra — swapping a processor in one dimension doesn't affect others. This is what makes variant isolation safe.

### Layer 2 — AEGIS: Adaptation Engine

AEGIS is a four-stage pipeline that runs on execution traces to propose and validate harness edits:

```
Digester   → parse traces; identify failure patterns and reward signals
Planner    → propose candidate harness edits targeting failure modes
Evolver    → apply edits in isolated variants; route tasks by cluster
Critic     → filter edits: reject reward hacking, forgetting, under-exploration
```

Each stage defends against a specific RL pathology:

| Pathology | Defended by |
|-----------|------------|
| Reward hacking | Critic: checks gains on held-out evaluation set |
| Catastrophic forgetting | Deterministic gating: edits only activate if above threshold |
| Under-exploration | Planner: ensemble routing ensures diverse variant coverage |

**Variant isolation via ensemble routing** is critical: a single harness can't satisfy contradictory task requirements. AEGIS routes tasks to per-cluster variants, preventing cross-task regressions.

### Layer 3 — Harness–Model Co-Evolution

Rather than alternating harness tuning and model training, HarnessX shares a **replay buffer** between both:

- Harness evolution generates diverse, high-signal trajectories
- Model trains via cross-harness GRPO across successive harness versions
- Model improvements generate better traces → better harness proposals → repeat

This breaks both ceilings: the harness keeps the model challenged; the model generates richer traces for the harness to learn from.

---

## Results

| Benchmark | Gain range | Notes |
|-----------|-----------|-------|
| ALFWorld | +11.2% – +44.0% | Weakest model gains most |
| GAIA | +9.7% – +17.1% | Global strategy stagnates; variant isolation unlocks +13.6% |
| WebShop | +13.0% – +18.0% | Consistent across models |
| τ³-Bench | +1.1% – +14.5% | Near-ceiling limits gains |
| SWE-bench Verified | +10.9% – +18.2% | Late-stage degradation observed |
| **Average** | **+14.5%** | 14 of 15 model–benchmark configs improve |

Co-evolution bonus: **+4.3% – +5.0%** additional gain over harness evolution alone.

**Inverse scaling**: weaker baseline models benefit most — harness evolution addresses gaps smaller models can't self-correct via prompting or RLHF.

---

## Key lessons

1. **Treat harnesses as evolvable code, not static config.** The harness is as much a target for optimisation as the model weights.
2. **Typed processors make variant isolation safe.** Without explicit scope boundaries, edits produce sub-threshold regressions that accumulate.
3. **Scalar reward is insufficient.** You need rich execution traces to detect reward hacking, under-exploration, and coupled failures.
4. **Don't alternate harness and model training — interleave them.** Separate loops leave both at a ceiling neither can escape independently.
5. **Heterogeneous tasks require ensemble routing.** One harness for all task types will compromise on everything.

---

## The RL framing

Once you see harness evolution as optimisation, the mapping to reinforcement learning is exact:

| RL concept | HarnessX equivalent |
|-----------|---------------------|
| State | The current harness version |
| Action | An AEGIS-proposed edit |
| Reward signal | Execution trace + benchmark score |
| Policy update | New harness version (gated) |
| Failure modes | Reward hacking, catastrophic forgetting, under-exploration |

This framing is not just aesthetic — it explains why the same failure modes that break model RL training show up when a system edits its own scaffolding, and why AEGIS's four stages map directly onto the defences RL practitioners already use (held-out eval, threshold gating, diverse exploration).

The result that matters: **weaker models benefit most.** An evolved harness closes gaps a weak model cannot fix in its weights. The weights never change — the environment around them gets smarter.

---

## Relation to other work

HarnessX extends the Loop Engineering pattern (see [Loop Engineering](../tips/loop-engineering.md)) — specifically, it automates the *evolver* and *verifier* roles that Karpathy's AutoResearch pattern suggests should be human-designed. The creator/verifier split maps directly onto AEGIS's Evolver/Critic stages.

---

## Source

- **Paper**: [arXiv:2606.14249](https://arxiv.org/abs/2606.14249)
- **Institution**: Anthropic
- **Code**: planned open-source release
