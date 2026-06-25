# Narrative Content in Pretraining Data: A Dimension Current Curation Ignores

> Source: [arXiv:2606.19468](https://arxiv.org/abs/2606.19468) · Jun 2026  
> Authors: Teagan Johnson, Elliott Ash, Andrew Piper, Maria Antoniak

## TL;DR

NarraBERT and NarraDolma introduce the first large-scale measurement of narrative content (agency, setting, events) across Dolma, a 3-trillion-token open pretraining corpus. Narrative qualities are unevenly distributed across pretraining sources — a dimension that current data curation practices neither measure nor account for, with implications for how models reason about stories and events.

---

## The problem

Pretraining data curation focuses on quality signals like language identification, deduplication, toxic content filtering, and source trust. But narrative structure — how much text involves agents acting in settings, with events unfolding over time — is never measured. This matters because:

- Models trained on more narrative-rich data may reason better about events, causality, and temporal sequences
- If narrative content is concentrated in certain sources (e.g., books) and absent in others (e.g., code, structured data), the source mix implicitly shapes what the model "knows" about the world
- No tools existed to measure this at scale

---

## How it works

**NarraBERT**: A RoBERTa-based classifier trained on 400 manually annotated passages to predict 11 narrative dimensions. Three core elements:
- **Agency**: Who acts, with what intentionality
- **Setting**: Where/when events occur
- **Events**: What happens, in what sequence

**NarraDolma**: The NarraBERT model applied to 3 million passages sampled from Dolma, producing a labeled dataset measuring narrative dimensions across all Dolma sources (web crawl, Wikipedia, arXiv, books, code, etc.).

Both NarraBERT and NarraDolma are publicly released.

---

## Results

Key findings from the NarraDolma analysis:

- Web text contains a "continuous, multidimensional narrative structure" — it's not simply narrative or non-narrative
- Narrative qualities vary significantly across sources: books score higher on agency/events; code and structured data score near zero
- Narrative distribution is unequal across topics within the same source
- Current curation pipelines have no mechanism to balance or even measure this distribution

---

## Why it matters for local AI

For practitioners training or fine-tuning open-weight models:

- **Data mix decisions**: If you're curating fine-tuning data, NarraBERT gives you a new axis for analysis — narrative density alongside existing quality signals
- **Capability gaps**: Models that reason poorly about temporal event sequences or causality may have been undertrained on narrative content, not undertrained in general
- **Evaluation**: NarraDolma provides a reference for what the narrative distribution of a large open corpus looks like, useful for comparing custom datasets

---

## Limitations

- NarraBERT trained on 400 passages — small annotation set; classifier quality on edge cases is uncertain
- Correlating narrative content with downstream task performance remains future work
- Analysis covers Dolma; other corpora (C4, RedPajama, FineWeb) may differ significantly

---

## Source

- **Paper**: [arXiv:2606.19468](https://arxiv.org/abs/2606.19468)
- **Preprint date**: Jun 2026
