# Strands Agents + LeRobot: Hub-to-Hardware Robotics

> Source: [Hugging Face Blog](https://huggingface.co/blog/amazon/strands-lerobot-hub-to-hardware) · AWS + HuggingFace · June 2026  
> License: Apache 2.0

## TL;DR

Strands Agents SDK (AWS) wraps LeRobot's robotics stack as composable agent tools, enabling a single agent to control robots in MuJoCo simulation and physical hardware with the same code. The HuggingFace Hub acts as the shared registry for datasets and policies — record in sim, push to Hub, deploy to hardware without reformatting.

---

## The two layers

### LeRobot (HuggingFace)
The robotics foundation layer — handles:
- Hardware abstraction and calibration
- Dataset format (`LeRobotDataset` — parquet + MP4)
- Policy training for open-weight robot policies
- Hardware drivers for physical robots (SO-101, etc.)

### Strands Agents SDK (AWS)
The orchestration layer — wraps LeRobot as **AgentTools**:
- Simulation control
- Dataset recording and upload
- Policy evaluation
- Multi-robot fleet coordination via Zenoh mesh networking

---

## The key insight: identical dataset format

A dataset captured in **MuJoCo simulation** and one captured from a **physical SO-101 robot** use identical on-disk formats — the same parquet schema and MP4 layout. Switching between sim and real is a single keyword argument:

```python
env = LeRobotEnv(mode="sim")   # MuJoCo
env = LeRobotEnv(mode="real")  # physical hardware
```

The agent code doesn't change. This eliminates the usual sim-to-real reformatting overhead.

---

## Workflow

```
Record demos in MuJoCo
        ↓
Push LeRobotDataset to HuggingFace Hub
        ↓
Train policy (ACT / Diffusion Policy / SmolVLA / π0)
        ↓
Evaluate policy in simulation
        ↓
Deploy to physical hardware (same agent code)
        ↓
Coordinate multi-robot fleets via Zenoh
```

---

## Supported open-weight policies

| Policy | Size | Notes |
|--------|------|-------|
| **ACT** (Action Chunking with Transformers) | — | Standard manipulation baseline |
| **Diffusion Policy** | — | Generative action prediction |
| **SmolVLA** | 0.5B | Lightweight vision-language-action |
| **π0 / π0.5** | — | Flow-matching; auto Real-Time Chunking |

Also supported via containerized inference: NVIDIA GR00T, Cosmos 3.

---

## Limitations

- Strands SDK requires AWS infrastructure for orchestration (not fully self-hostable)
- Physical hardware support focused on SO-101 and compatible arms
- Fleet coordination (Zenoh) adds networking complexity for multi-robot setups

---

## Source

- **Blog**: [From the HuggingFace Hub to robot hardware with Strands Agents and LeRobot](https://huggingface.co/blog/amazon/strands-lerobot-hub-to-hardware)
- **LeRobot**: [huggingface/lerobot](https://github.com/huggingface/lerobot)
- **Strands SDK**: [strands-agents/strands-agents-sdk](https://github.com/strands-agents/sdk)
