# Current World Models Lack a Persistent State Core

> Source: [arXiv:2606.20545](https://arxiv.org/abs/2606.20545) · June 2026  
> Authors: Jinpeng Lu, Dexu Zhu, Haoyuan Shi, Linghan Cai, Guo Tang, Yinda Chen, Jie Cao, Duyu Tang, Yi Zhang, Yong Dai, Xiaozhu Ju

## TL;DR

Current video-generation-based world models fail to maintain persistent state when objects leave the frame — they simply resume objects in their original state rather than evolving them forward. WRBench, a diagnostic benchmark testing 23 models on 9,600 videos, reveals this is a fundamental architectural gap that scaling and improved image quality alone cannot fix.

---

## The problem

Video generation models are increasingly used as world models — systems that understand and predict how the world evolves. But they have a critical blindspot: **they cannot maintain internal state for objects that leave the frame**.

When you move a camera away from an object and then pan back, a world model should know:
- Where is the object now?
- How has it moved since the camera left?
- Is it in a different state than before?

Instead, current models act like a tracking shot: when the camera returns, they resume the object *in its original state* as if time hadn't passed. They lack "an internal world state that keeps evolving over time, decoupled from observation."

This isn't a minor edge case — it's a fundamental architectural limitation across the field.

---

## WRBench: Diagnostic benchmark

WRBench is the first systematic benchmark for diagnosing persistent state in world models. It treats camera movement as an observability intervention and evaluates three core questions:

1. **Camera control**: Does the model execute the requested camera interactions correctly?
2. **Scene continuity**: While the camera is on target, does the scene remain spatially and temporally consistent?
3. **Persistent state**: When the camera returns to a previously seen object, does it reflect the correct state given the elapsed time and prior motion trajectory?

The benchmark tested:
- **23 different video generation models** (various architectures and scales)
- **9,600 videos** across four control paradigms
- **Consistent failure**: *none of the models reliably maintain object state across occlusions*

---

## Key findings

### Models fail across all scales and architectures

The limitation isn't restricted to smaller models — it appears in state-of-the-art systems regardless of parameter count. Scaling alone does not solve the problem.

### Scaling doesn't fix it

Larger models and better image generation quality don't automatically produce persistent state. The failure is structural, not a matter of insufficient capacity or training data quantity.

### Dedicated state mechanisms are required

The research shows that robust world-state persistence requires **making it a primary design objective**. This means:
- Explicit internal state representations that evolve independently of observations
- Architectural mechanisms to maintain and update hidden state over unobserved intervals
- Validation that state propagates correctly when new observations resume

---

## Why it matters

World models are increasingly important for:
- **Robotics and embodied AI** — agents need to predict consequences of actions on unobserved objects
- **Planning and reasoning** — systems must maintain a coherent model of the world even when parts become hidden
- **Video understanding and generation** — both require understanding that the world continues to exist beyond what's visible

The current architectural gap means existing video-based world models cannot reliably:
- Predict what happens to occluded objects
- Plan actions that depend on hidden state
- Maintain causal consistency in complex scenes

Fixing this requires rethinking how world models represent and evolve internal state, not just scaling existing approaches.

---

## Source

- **Paper**: [arXiv:2606.20545](https://arxiv.org/abs/2606.20545)
