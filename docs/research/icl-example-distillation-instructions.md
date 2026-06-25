# ICL Example Distillation: 99% Token Reduction Without Accuracy Loss

> Source: [arXiv:2606.15641](https://arxiv.org/abs/2606.15641) · Jun 2026  
> Authors: Guy Rotman, Adi Kopilov, Danit Berger Zalmanson, Omri Allouche

## TL;DR

Instead of including raw few-shot examples in prompts, this work converts them into compact structured task instructions — achieving 99% token reduction while improving macro-averaged AUC by up to 7% on a new B2B conversation benchmark. Unlike token compression methods (which degrade as context grows), distilled instructions remain stable.

---

## The problem

In-context learning relies on few-shot examples that are long, verbose, and expensive to include at inference time. For production systems handling hundreds of categories (e.g., B2B conversation classification), prompt lengths become unmanageable. Standard compression baselines degrade by over 9 F1 points as context size increases.

The deeper issue: few-shot examples contain both the *signal* (what distinguishes classes) and *noise* (stylistic variation, irrelevant context). Including raw examples passes both to the model.

---

## How it works

The key idea: extract the knowledge from examples and encode it as explicit structured criteria, rather than letting the model infer it from raw examples at inference time.

**Distillation process:**
1. Collect labeled examples per class
2. Use an LLM to extract discriminative criteria from examples (what makes each class distinct)
3. Synthesize these into compact, structured task instructions — precise classification rules

At inference time, the prompt contains only the distilled instructions, not the original examples. The model classifies using the extracted criteria directly.

**Call Playbook Benchmark**: Introduced alongside the paper — five classification tasks on real B2B conversations covering phenomena like objection handling, intent detection, and conversation stage.

---

## Results

| Metric | Traditional ICL | Distilled Instructions |
|---|---|---|
| Token usage | Baseline | −99% |
| Macro-averaged AUC | Baseline | +up to 7% |
| Stability as context grows | Degrades >9 F1 pts | Stable |

Advanced compression baselines (which try to shorten raw examples) still degrade as context grows — distillation to instructions avoids this because the instructions don't grow with the number of examples.

---

## Why it matters for local AI

This technique directly addresses a practical constraint in local inference:

- **Context window pressure**: Local models have limited context; 99% token reduction makes multi-class classification feasible on 8K-context models
- **Inference speed**: Shorter prompts mean lower TTFT and cost per call, especially important for high-throughput local deployments
- **Generalizability**: The approach isn't domain-specific — any classification task with labeled examples can apply example distillation
- Works with any LLM; no fine-tuning required

---

## Limitations

- Distillation quality depends on the LLM used to extract criteria — smaller models may produce worse instructions
- Evaluated on conversation classification; performance on other task types is unknown
- The distillation step itself has an upfront cost (run once per task, not per inference)

---

## Source

- **Paper**: [arXiv:2606.15641](https://arxiv.org/abs/2606.15641)
- **Preprint date**: Jun 2026 (ACL 2026 Findings)
