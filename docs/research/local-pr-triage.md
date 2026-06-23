# Local Open-Weight Models for Real-Time PR Triage

> Source: [Hugging Face Blog](https://huggingface.co/blog/local-models-pr-triage) · 2026

## TL;DR

HuggingFace built a fully local PR triage system for the OpenClaw repository using open-weight models (Qwen, Gemma, DeepSeek) with sandboxed shell access. The system achieves 83.1% precision with Qwen3.6-35B without fine-tuning, processes PRs in real time, and costs only electricity—no cloud API fees. Reposhell (a restricted read-only shell) lets models inspect repository context safely.

---

## The Problem

The OpenClaw repository receives hundreds of PRs and issues daily. Real-time triage requires instant categorization without cloud API quotas or batch processing delays. Previous approaches either:
- Depend on cloud APIs with rate limits
- Batch-process every 2–6 hours, delaying notifications
- Incur per-inference subscription costs

---

## System Design

### Architecture

A semi-agentic pipeline with five components:

1. **Local GitHub mirror** — via `openclaw/gitcrawl`, keeping PR and repository data locally accessible
2. **SQLite job queue** — scheduling triaging tasks deterministically
3. **Classification agent** — runs locally on a restricted sandboxed shell (reposhell)
4. **Discord notifications** — real-time alerts based on classification results
5. **Validation audit** — periodic checkpoints using cloud models (GPT-5.5) every 2 hours for calibration

### Reposhell: Sandboxed Repository Context

Models can inspect repository context via a restricted bash-like shell limiting operations to read-only commands:

```
pwd, ls, find, rg, grep, sed -n, cat, head, tail, wc -l, 
git status, git show, git grep, git ls-files
```

This allows the model to:
- Search code and commit history
- Inspect file structure and changes
- Extract relevant context from PR diffs and related files

But prevents:
- Unsafe command execution
- Network calls
- File modifications

---

## Models & Results

Three open-weight models were tested on a 330-row evaluation set from dutifuldev/openclaw-classification-dataset (639 entries total):

| Model | Params | Active | Precision | Recall | F1 Score | Latency (s/row) |
|-------|--------|--------|-----------|--------|----------|-----------------|
| Gemma 4 | 26B | 4B | 0.716 ± 0.010 | 0.905 ± 0.004 | 0.800 ± 0.008 | 1.41 ± 0.04 |
| Qwen 3.6 | 35B | 3B | 0.831 ± 0.007 | 0.818 ± 0.006 | 0.824 ± 0.002 | 13.51 ± 0.79 |
| DeepSeek V4-Flash | 284B | 13B | 0.938 | 0.714 | 0.811 | 144.14 |

### Key Observations

- **Qwen achieved the best balance** between precision, recall, and latency for real-time use
- **Gemma showed highest throughput** — 402.6 aggregate tokens/second, reaching 700+ tokens/sec with optimizations (vLLM, NVFP4 quantization, prefix caching)
- **DeepSeek maximized precision** at the cost of latency; used as a reference point
- **No fine-tuning required** — agentic setup with shell access is sufficient for effective classification

### Hardware & Cost

- **Hardware**: NVIDIA DGX Spark (Blackwell) with 128GB unified memory
- **Inference cost**: Electricity only; local models run with zero per-inference fees
- **Validation audit**: ~$9/month using cloud models (GPT-5.5) for periodic calibration during transition
- **Throughput**: Gemma reached 700+ tokens/second with vLLM, quantization, and prefix caching

---

## Key Takeaways

1. **Agentic setup is sufficient** — No fine-tuning needed when models have sandboxed access to repository context via shell commands

2. **Local inference eliminates cloud overhead** — Real-time triage with zero per-inference API costs; only electricity expense

3. **Smaller models are pragmatic** — Qwen3.6-35B (3B active) delivers strong precision/recall trade-off with 50× lower latency than larger alternatives

4. **Hardware optimization matters** — Quantization (NVFP4), serving frameworks (vLLM), and prefix caching unlock significant throughput improvements

5. **Broader applications** — The pattern applies to news categorization, customer support triage, content moderation, and any task requiring repository/document context

6. **Validation bridge strategy** — Using a larger cloud model as a periodic judge (every 2 hours) is cost-effective during the transition from manual to fully local evaluation

---

## Code & Data

- **Main project**: [localpager](https://github.com/osolmaz/localpager)
- **Evaluation repository**: [onurclaw](https://github.com/osolmaz/onurclaw)
- **Dataset**: dutifuldev/openclaw-classification-dataset (639 labeled PR entries)
