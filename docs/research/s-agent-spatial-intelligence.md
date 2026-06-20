# S-Agent: Spatial Tool-Use Elicits Reasoning for Spatial Intelligence

> Source: [arXiv:2606.20515](https://arxiv.org/abs/2606.20515) · June 2026  
> Authors: Yalun Dai, Hao Li, Shulin Tian, Runmao Yao, Yuhao Dong, Fangzhou Hong, Zhaoxi Chen, Fangfu Liu, Baoliang Tian, Dingwen Zhang, Tao Wang, Kim-Hui Yap, Ziwei Liu

## TL;DR

Vision-language models struggle with spatial reasoning because they process single frames independently. S-Agent introduces a hierarchical tool architecture where a semantic planner coordinates specialized 2D grounding, 3D lifting, and spatial reasoning tools. The distilled 8B model reaches **41.6% on MMSI-Bench**, competing with GPT-4.5 and Gemini 2.0, by accumulating evidence across multiple viewpoints and reasoning steps.

---

## The problem

Spatial understanding requires integrating evidence across multiple perspectives — counting objects in a scene, reasoning about depths, understanding geometric relationships. But standard VLMs process images frame-by-frame without explicit mechanisms to ground spatial concepts or accumulate geometric evidence.

Existing approaches either:
- Process single frames in isolation, losing 3D context
- Require full model retraining to add reasoning capabilities
- Struggle to ground abstract spatial relationships into concrete 2D/3D evidence

---

## S-Agent Framework

**Core insight**: Separate *semantic planning* (what evidence is needed?) from *spatial evidence acquisition* (2D grounding, 3D geometry, reasoning).

### Hierarchical Tool Architecture

The system operates as an agent with a VLM as the semantic planner and specialized spatial tools:

| Tool | Role |
|------|------|
| **2D Grounding** | Locates objects in image coordinates; grounds language references to pixel regions |
| **3D Lifting** | Infers 3D geometry from 2D observations (depth, position, orientation) |
| **Spatial Reasoning** | Aggregates evidence across frames to solve counting, comparison, and relationship tasks |

### Memory Systems

- **Scene Memory**: Maintains an evolving representation of the scene state (objects, their 3D positions, attributes)
- **Agent Memory**: Accumulates reasoning context across tool calls and inference steps, enabling multi-step spatial reasoning

### Training: S-300K Dataset & Distillation

Rather than inference-time enhancement alone, the team created **S-300K**, a dataset of spatial reasoning trajectories showing how the agent uses tools to solve problems.

**S-Agent-8B** is trained via supervised fine-tuning on S-300K, distilling the hierarchical reasoning approach into a compact, deployable model. During inference, it can work with or without the tool framework.

---

## Key results

**MMSI-Bench benchmark** (multi-view spatial intelligence):

- **S-Agent-8B**: 41.6% accuracy
- **GPT-4.5**: ~40% (closed-source baseline)
- **Gemini 2.0 Flash**: ~42% (closed-source baseline)

Open-source model (8B parameters) matches cutting-edge proprietary systems on spatial reasoning without requiring model retraining during deployment.

### Generalization

The framework improves both:
- **Open-source VLMs** without retraining (inference-time tool use)
- **Closed-source models** (can run S-Agent-8B as a specialized component)

Consistent gains across different vision architectures, suggesting the tool structure is learnable and reusable.

---

## Why it matters

1. **Spatial reasoning is a teachable skill.** The hierarchical tool structure codifies how humans reason spatially — locate objects, infer 3D structure, aggregate evidence. This structure generalizes.

2. **Tool-use as a reasoning primitive.** By separating planning from execution, the system makes spatial reasoning steps explicit and interpretable. This is closer to how humans solve spatial problems.

3. **Inference-time enhancement without retraining.** The framework applies to existing VLMs and proprietary models, enabling rapid deployment without access to model weights.

4. **Open-weight competitive performance.** An 8B distilled model reaches GPT-4.5 / Gemini 2.0 Flash levels on spatial tasks — meaningful for inference cost and privacy-critical applications.

5. **Multi-view integration as a design pattern.** Scene Memory and Agent Memory show how to accumulate evidence across frames and reasoning steps, applicable beyond spatial tasks to any multi-step visual reasoning.

---

## Source

- **Paper**: [arXiv:2606.20515](https://arxiv.org/abs/2606.20515)
