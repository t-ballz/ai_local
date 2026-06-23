# Duration-Aware Scheduling for ASR Serving Under Workload Drift

> Source: [arXiv:2603.11273](https://arxiv.org/abs/2603.11273) · March 2026  
> Authors: Darshan Makwana, Yash Jogi, Harsh Kotta, Aayush Kubba

## TL;DR

Audio duration is a strong, reliable predictor of Whisper processing time. Replacing first-come-first-served (FCFS) scheduling with shortest-job-first (SJF) or highest-response-ratio-next (HRRN) algorithms in vLLM's scheduler reduces median latency by up to 73% (SJF) or 28% (HRRN with bounded tail latency). Practical for local Whisper serving setups where request duration varies significantly.

---

## The Problem

Speech recognition services receive requests with highly variable audio duration. A 10-second clip and a 5-minute recording have vastly different processing times, but most serving engines (including vLLM) use FCFS scheduling, treating all requests equally.

**FCFS + variable processing time = head-of-line blocking:**
- Short requests queue behind long-running transcriptions
- A 5-minute audio blocks all subsequent requests until it completes
- High overall latency even when the queue is mostly short clips
- **Workload drift** (changing distribution of request types over time) makes this worse — sudden bursts of long audio cause cascading delays

---

## Core Insight: Duration Predicts Latency

The paper demonstrates empirically that **audio duration has a strong linear relationship with transcription time** in Whisper models. This means:

1. You can predict request completion time at arrival (before processing)
2. Scheduling decisions can exploit this predictability
3. Reordering becomes a practical optimization lever

---

## Scheduling Algorithms Compared

### FCFS (First-Come-First-Served) — Baseline
- Process requests in arrival order
- Simple, fair, but ignores request characteristics
- Heavy tail latency under variable duration workloads

### SJF (Shortest-Job-First)
- Prioritize short-duration audio
- **Reduces median latency by up to 73% at high load**
- **Trade-off: increases tail latency (90th percentile) by up to 97%**
- Starvation risk: long-duration requests may wait indefinitely under continuous short requests

### HRRN (Highest-Response-Ratio-Next)
- Hybrid approach: prioritize short jobs *and* aging
- **Reduces median latency by up to 28%**
- **Bounds tail-latency degradation to at most 24%**
- Prevents starvation; fair aging mechanism ensures long requests eventually run
- **More balanced overall performance**

---

## How HRRN Works

HRRN calculates a response ratio for each waiting request:

```
response_ratio = (wait_time + service_time) / service_time
```

**Next request = highest response ratio.**

This means:
- **New short requests**: low ratio (high priority)
- **Old short requests**: medium ratio (aging effect)
- **Old long requests**: high ratio (eventually get priority)

Result: short jobs get throughput advantage, but long jobs don't starve.

---

## Implementation in vLLM

The researchers integrated both SJF and HRRN into vLLM's request scheduler. vLLM is widely used for local LLM/multimodal serving, and ASR workloads fit the same batching patterns:

1. **Scheduler modification**: replace FCFS queue with priority queue (SJF or HRRN)
2. **Duration estimation**: use audio duration (already known at request arrival)
3. **Batch formation**: batch shorter requests together, reducing head-of-line blocking
4. **No architectural changes**: works with existing vLLM infrastructure

---

## Results Summary

| Metric | FCFS | SJF | HRRN |
|--------|------|-----|------|
| Median latency (high load) | Baseline | **-73%** | **-28%** |
| 90th-percentile latency | Baseline | +97% | +24% |
| Practical for production | ✓ | ⚠ (starvation) | ✓ |

**Takeaway**: HRRN offers the best real-world balance — meaningful median improvement with tolerable tail-latency cost and fairness guarantees.

---

## Applying This Locally

If you run Whisper (or any ASR model) locally for batch transcription, duration-aware scheduling is directly applicable:

### Scenario 1: Local Transcription API
Use vLLM or similar serving framework with HRRN scheduler:
```bash
# vLLM with custom scheduler (once patched)
vllm serve openai/whisper-large-v3-turbo \
  --scheduler-type hrrn \
  --gpu-memory-utilization 0.8
```

### Scenario 2: Batch Processing Pipeline
If processing requests offline (not real-time):
1. **Sort by duration** before batching (SJF approach, no starvation risk)
2. **Batch short clips together** — minimize GPU downtime
3. **Process long clips separately** — they don't block the pipeline

### Scenario 3: Hybrid (Quorum + HRRN)
- Use HRRN as primary scheduler
- Ensure minimum throughput for long audio (aging mechanism)
- Suitable for mixed workloads (user uploads + internal batch jobs)

---

## Limitations & Caveats

- **Audio duration ≠ perfect predictor**: model variant, language, and audio quality affect latency; duration is strong but not perfect
- **Batch overhead**: prioritization adds CPU overhead to scheduler itself (minimal but non-zero)
- **Workload shift**: if distribution of audio length changes drastically, relative benefits may vary
- **Not tested on edge cases**: extremely short (<1s) or long (>1hr) audio may have different duration-latency relationships

---

## Key Takeaway

For local Whisper deployments with variable request sizes, **switching from FCFS to HRRN scheduling is a high-ROI optimization**. No model changes, no retraining, no new hardware — just reorder the work based on a simple, predictable property (audio duration). Especially useful if you notice latency spikes when long audio arrives.

---

## Source

- **Paper**: [arXiv:2603.11273](https://arxiv.org/abs/2603.11273)
- **Related**: [Whisper Large V3 Turbo](../models/whisper-large-v3-turbo.md) for local inference options
- **vLLM**: [vLLM Project](https://github.com/vllm-project/vllm)
