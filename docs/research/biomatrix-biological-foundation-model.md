# BioMatrix: Open-Weight Biological Foundation Model Across Sequences, Structures, and Language

> Source: [arXiv:2606.22138](https://arxiv.org/abs/2606.22138) · Jun 2026  
> Authors: Qizhi Pei, Zhimeng Zhou, Yi Duan, Yiyang Zhao, Wei Li, Han Guo, Liang He, Chengping Li, Chang-Yu Hsieh, Conghui He, Rui Yan, Lijun Wu

## TL;DR

BioMatrix is an open-weight biological foundation model (1.7B and 4B, built on Qwen3) that integrates molecular sequences (SMILES/SELFIES), molecular structures, protein sequences, protein structures, and natural language in a single decoder-only architecture. Pretrained on 304B tokens across all modalities, it achieves SOTA or competitive performance on 77 of 80 tasks without modality-specific heads or external encoders.

---

## The problem

Biology sits at the intersection of multiple data modalities: molecules are described by sequences (SMILES), 3D structures, and natural language; proteins have sequences, folded structures, and literature annotations. Existing models handle one or two modalities (ESM for protein sequences, ChemBERT for molecules) but can't reason across them jointly.

Multi-modal biological reasoning — "what protein structure would bind this molecule?" or "explain the mechanism of this drug-receptor interaction in natural language" — requires joint understanding that single-modality models can't provide.

---

## How it works

**Architecture**: Single decoder-only transformer (Qwen3 backbone) with unified tokenization that maps all five modalities into a shared discrete token space.

- No external encoders, projection adapters, or modality-specific output heads
- All modalities processed via next-token prediction — the same objective for sequences, structures, and language
- Structures (3D coordinates) are tokenized into discrete tokens via modality-specific tokenizers before entering the shared decoder

**Modalities**:
| Modality | Representation |
|---|---|
| Molecular sequences | SMILES and SELFIES notation |
| Molecular structures | 3D coordinate tokenization |
| Protein sequences | Amino acid sequences |
| Protein structures | Structure tokens (via structure tokenizer) |
| Natural language | Standard text |

**Training data**: 304.4B tokens including general text, domain scientific text, sequence/structure views of molecules and proteins, and cross-modal corpora with interleaved biomolecular-scientific text.

**Model sizes**: 1.7B and 4B parameters — both available on HuggingFace.

---

## Results

| Evaluation scope | Performance |
|---|---|
| 80 tasks spanning 6 categories | SOTA or competitive on **77/80** |
| Task categories | Single/multi-entity understanding + generation across all modalities |

---

## Why it matters for local AI

- **Open weights, both sizes on HuggingFace**: Directly downloadable for local drug discovery, protein analysis, or bioinformatics research
- **Unified architecture**: No need to run separate protein model + chemistry model + text model and stitch outputs together — one model handles the full pipeline
- **Qwen3 base**: Benefits from Qwen3's strong language reasoning capabilities, potentially enabling cross-modal scientific reasoning that pure biology models lack
- **Instruction following**: Built on a chat-tuned base, so natural language queries about molecules/proteins are supported

---

## Limitations

- Specialized domain — primarily useful for computational biology, drug discovery, structural bioinformatics
- Structure tokenization quality bounds performance on 3D tasks — not a continuous 3D representation
- 4B maximum size; large protein complexes or full-genome reasoning may require larger models

---

## Source

- **Paper**: [arXiv:2606.22138](https://arxiv.org/abs/2606.22138)
- **Preprint date**: Jun 2026
