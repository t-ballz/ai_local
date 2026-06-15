# FastContext

> Source: [github.com/microsoft/fastcontext](https://github.com/microsoft/fastcontext) · [arxiv.org/abs/2606.14066](https://arxiv.org/abs/2606.14066) · [HuggingFace: microsoft/FastContext-1.0-4B-SFT](https://huggingface.co/microsoft/FastContext-1.0-4B-SFT) · June 15, 2026

## TL;DR

Microsoft's specialized **repository-exploration subagent** for coding agents. Instead of letting the main agent (GPT-5.4, etc.) burn tokens searching through codebases, a small FastContext model handles all READ / GLOB / GREP calls and returns compact citations. Result: **up to +5.5 score on SWE-bench** and **up to 60% fewer main-agent tokens**. Runs at 4B or 30B; MIT licence.

---

## The problem it solves

In real coding-agent trajectories (analysed on GPT-5.4), repository exploration dominates:

| Activity | Share of tool-use turns | Share of main-agent tokens |
|----------|------------------------|--------------------------|
| Reading + searching code | 56.2% | 46.5% |
| Everything else | 43.8% | 53.5% |

A general-purpose frontier model is expensive for this work. FastContext replaces it with a small model trained specifically to navigate repos efficiently and return only the relevant file paths and line ranges.

---

## Specs

| Property | FastContext 4B | FastContext 30B |
|----------|---------------|----------------|
| Base model | Qwen3-4B-Instruct | Qwen3-Coder-30B-A3B (MoE) |
| Active params | 4B | ~3B (MoE) |
| Context | 262K tokens | 262K tokens |
| Format | BF16 (safetensors) | BF16 (safetensors) |
| Variants | SFT, RL | SFT |
| Licence | MIT | MIT |

**HuggingFace**: `microsoft/FastContext-1.0-4B-SFT` · `microsoft/FastContext-1.0-4B-RL`

---

## How it works

FastContext runs as a subagent called by the main coding agent whenever codebase exploration is needed. It loops through three steps:

1. **Query understanding** — translates the issue/task into concrete search objectives
2. **Parallel tool calls** — issues simultaneous READ / GLOB / GREP operations to cover multiple hypotheses
3. **Observation-driven refinement** — uses intermediate results to steer subsequent searches

Final output is a **citation block**: a structured list of file paths + line ranges for the main agent to pass directly to its context. The main agent never sees the raw search noise.

**Tools exposed to FastContext** (read-only):

| Tool | What it does |
|------|-------------|
| `READ` | Returns line-numbered file content |
| `GLOB` | Discovers paths matching a pattern |
| `GREP` | Regex search across the repo (ripgrep-style) |

---

## Training

1. **SFT** — fine-tuned on curated exploration traces demonstrating parallel tool calling, multi-turn evidence gathering, and citation generation
2. **RL** — deployed as the actual subagent; optimised with GRPO using rewards based on:
   - File-level and line-level F1 score (did it find the right code?)
   - Parallel exploration bonus (penalises sequential one-by-one searching)
   - Format penalties

FC-4B-RL matches or beats FC-4B-SFT on all reported benchmarks.

---

## Benchmarks

FastContext plugged into **Mini-SWE-Agent** style scaffold. Main agent column shows which LLM drives the solve step.

| Benchmark | Main agent | Score Δ | Token savings |
|-----------|-----------|---------|---------------|
| SWE-bench Multilingual | GPT-5.4 | +3.3% | −22.1% |
| SWE-bench Pro | GPT-5.4 | +3.0% | −15.9% |
| SWE-QA | GPT-5.4 | +0.7% | **−50.7%** |
| SWE-bench Pro | GLM-5.1 | +5.0% | — |
| SWE-bench Pro (best) | — | **+5.5%** | up to −60.3% |

SWE-QA has the largest token savings because it involves wide repo reading with a narrow answer — exactly what FastContext is designed for.

---

## Running locally

**SGLang** (recommended for production):

```bash
python3 -m sglang.launch_server \
    --model-path microsoft/FastContext-1.0-4B-SFT \
    --tool-call-parser qwen \
    --context-length 262144 \
    --trust-remote-code \
    --dtype bfloat16
```

**vLLM**, **Ollama**, and **llama.cpp** are also supported per the model card.

!!! note "Integration pattern"
    FastContext is a subagent, not a standalone model. The main coding agent detects exploration steps and delegates them to the FastContext server via tool calls — see the [GitHub repo](https://github.com/microsoft/fastcontext) for the integration harness.

---

## Source & licence

- **Licence**: MIT
- **Weights**: [microsoft/FastContext-1.0-4B-SFT](https://huggingface.co/microsoft/FastContext-1.0-4B-SFT) (also 4B-RL, 30B-SFT)
- **Code**: [github.com/microsoft/fastcontext](https://github.com/microsoft/fastcontext)
- **Paper**: [arxiv.org/abs/2606.14066](https://arxiv.org/abs/2606.14066)
