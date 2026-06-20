# Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages

> Source: [arXiv:2606.20517](https://arxiv.org/abs/2606.20517) · June 2026  
> Authors: Maria Ivanova, Pavel Zadorozhny, Rodion Levichev, Ivan Petrov, Adamenko Pavel, Ivan Lopatin, Alexey Kutalev, Dmitrii Babaev

## TL;DR

Multi-LCB extends LiveCodeBench from Python to 12 programming languages (C++, C#, Java, JavaScript, TypeScript, Go, Rust, Ruby, PHP, Kotlin, Scala) to reveal that Python proficiency does not transfer to polyglot coding. Testing 24 LLMs shows ~20 percentage points performance drop from Python to lower-scoring languages, exposing "language-specific contamination" and substantial multilingual capability gaps.

---

## The problem

LiveCodeBench evaluates coding ability on algorithmic tasks in Python, but real-world deployment requires multilingual support. A critical blind spot: **models strong in Python may be weak in other languages**, and we have no benchmark to measure this disparity. Existing evaluations either stick to Python or lack contamination controls, making it unclear whether performance gains reflect genuine capability or training data leakage.

---

## Method: Systematic language expansion with contamination controls

**Benchmark design:**
- Converted identical algorithmic tasks from Python to 12 target languages
- Maintained task semantics and difficulty across all versions
- Unified STDIN/STDOUT evaluation harness — all languages use the same I/O interface

**Contamination mitigation:**
- Tracking future updates ensures consistent task freshness across languages
- Designed to prevent train-test leakage by using freshly generated tasks with known creation dates

**Evaluation scope:**
- 24 LLMs tested (spanning size and training philosophies)
- Identical algorithmic problems converted across all languages
- Pass@1 as primary metric to assess zero-shot performance

---

## Key results

**Python remains the strongest language:**
- Python Pass@1: **48.2%** (baseline)
- Scala: **~29%** (largest gap, ~19pp drop)
- Consistent 15–20pp performance degradation from Python to weakest-performing languages

**Python proficiency ≠ polyglot strength:**
- Models ranking highly on Python tasks do not necessarily maintain their relative ranking across other languages
- Performance varies unpredictably by language and model — suggesting language-specific training data effects dominate

**Language-specific disparities:**
- Evidence of training data contamination patterns that differ by language
- Some languages (C++, Java) perform closer to Python; others (Scala, Kotlin, Ruby) lag significantly
- The gap persists even for large, well-trained models

---

## Why it matters

**For model developers:**
- Published benchmarks (often Python-only) can mask critical gaps in multilingual capability
- Training coverage and contamination vary by language — optimizing for one language may degrade others

**For deployment:**
- Organizations requiring polyglot coding support cannot rely on Python eval as a proxy
- Need explicit multilingual evaluation to match real system requirements

**For research:**
- Reveals that model generalization is more brittle than single-language metrics suggest
- Demonstrates that a unified benchmark framework (same tasks, same I/O harness) can reliably expose hidden weaknesses
- Opens investigation into why certain language pairs show larger gaps (Python → Scala vs. Python → Java)

---

## Source

- **Paper**: [arXiv:2606.20517](https://arxiv.org/abs/2606.20517)
