# Notes2Skills: From Lab Notebooks to Certainty-Aware Agent Skills

> Source: [arXiv:2606.11897](https://arxiv.org/abs/2606.11897) · Jun 2026  
> Authors: Shi Liu, Jiayao Chen, Chengwei Qin, Yanqing Hu, Jufan Zhang, Linyi Yang

## TL;DR

Notes2Skills extracts executable agent skills from informal laboratory notebooks while preserving the author's certainty level — distinguishing tentative observations from confirmed conclusions. Without this certainty-preservation, extracted skills confuse uncertain hypotheses with reliable facts, producing unsafe AI collaboration in scientific workflows.

---

## The problem

Laboratory notebooks are rich with scientific knowledge, but they mix registers: confirmed results, tentative interpretations, open questions, and speculative plans all appear in the same prose. When an AI agent extracts skills from these notebooks naively, it treats "I suspect the yield decreases with temperature" the same as "Yield decreases 12% per 10°C (confirmed, n=8)."

This conflation produces skills that overstate reliability — the agent takes confident actions on uncertain premises, which in a laboratory context can mean ruined experiments, wasted reagents, or unsafe procedures.

---

## How it works

**Two-stage framework**:

1. **Certainty detection**: A classification stage that labels each assertion in the notebook with a certainty level — confirmed, probable, speculative, or unknown. The classifier is trained to detect hedging language, conditional framing, and evidential markers.

2. **Certainty-conditioned skill extraction**: Extracted skills carry their certainty level as metadata. A confirmed procedure becomes an executable skill; a speculative hypothesis becomes a conditional skill with explicit uncertainty markers that the agent surfaces before acting.

The result: agents can reason over the *reliability* of skills, not just their content — falling back to human confirmation when certainty is low.

---

## Results

Human evaluation on scientific lab notebook corpora shows that certainty preservation is the critical missing component between raw notebook text and reliable agent skills. Skills extracted without certainty awareness consistently conflate uncertain claims with confirmed facts.

---

## Why it matters for local AI

Scientific AI agents (lab automation, literature synthesis, hypothesis generation) are a growing use case for local models. Notes2Skills provides the infrastructure to ground these agents in actual experimental evidence rather than unvetted claims. The certainty-preservation pattern applies broadly to any domain where information sources mix confirmed and speculative content — maintenance logs, engineering notebooks, medical notes.

---

## Limitations

- Certainty detection relies on linguistic markers; domain-specific conventions (e.g., statistical thresholds used differently across fields) may cause misclassification
- Framework requires lab notebooks in structured or semi-structured text form; handwritten or highly informal notes need preprocessing
- Evaluation is on scientific domain notebooks; transfer to other informal writing styles untested

---

## Source

- **Paper**: [arXiv:2606.11897](https://arxiv.org/abs/2606.11897)
- **Preprint date**: Jun 2026
