# Unlimited OCR Works: Reference Sliding Window Attention for Long-Document OCR

> Source: [arXiv:2606.23050](https://arxiv.org/abs/2606.23050) · Jun 2026  
> Authors: Youyang Yin, Huanhuan Liu, Qunyi Xie, Chaorun Liu, Shiqi Yang, Shaohua Wang, Zhanlong Liu, Hao Zou, Jinyue Chen, Shu Wei, Jingjing Wu, Mingxin Huang, Zhen Wu, Guibin Wang, Tengyu Du, Lei Jia

## TL;DR

Reference Sliding Window Attention (R-SWA) replaces standard decoder attention with a mechanism that constrains attention to a fixed set of reference visual tokens plus a sliding window of recent outputs, keeping KV cache size constant throughout decoding. Built on DeepSeek OCR, the system transcribes 40+ page documents in a single forward pass with constant memory — eliminating the per-page batching required by standard OCR models.

---

## The problem

LLM-based OCR models generate text token by token, and the KV cache grows with every output token. For a 40-page document, the accumulated KV cache becomes enormous — memory consumption spikes and generation slows dramatically as the document progresses. Standard solutions (chunking, sliding window over input) introduce boundary artifacts and can't handle cross-page context.

---

## How it works

**Reference Sliding Window Attention (R-SWA)**:

Instead of attending to the full KV cache (which grows with output length), each decoder step attends to:
- **Reference visual tokens**: A fixed set of encoded image representations from the input — these don't grow with output length
- **Sliding window of recent output tokens**: A fixed-size window of the most recent generated tokens for local coherence

The KV cache stays constant throughout the entire decoding process, regardless of document length. This mimics how humans transcribe text: referencing the source image plus short-term working memory, not re-reading all previous output.

**Base model**: DeepSeek OCR provides the visual encoder and initial decoder weights; R-SWA replaces the decoder's standard attention layers.

**Single-pass operation**: Under a standard 32K maximum sequence length, the model transcribes dozens of pages without batching or chunking — each page's content informs interpretation of surrounding pages.

---

## Results

| Metric | Result |
|---|---|
| OmniDocBench v1.5 | 93% accuracy |
| Document length | 40+ pages in single forward pass |
| Memory scaling | Constant (does not grow with document length) |

---

## Why it matters for local AI

Long-document OCR is a practically important capability for local deployment:

- **Research workflows**: Digitizing books, papers, historical documents, legal filings — all multi-page
- **Document RAG**: Processing entire PDFs rather than chunking by page boundary (which breaks tables and figures that span pages)
- **Constant memory**: Predictable resource usage regardless of document length makes deployment planning straightforward
- **R-SWA pattern**: The reference tokens + sliding window approach is applicable to any sequence generation task with a static "source" that should be attended throughout — image captioning, audio transcription, code generation from a spec

---

## Limitations

- 32K sequence length limit: extremely long documents (100+ pages) still require batching
- Reference token selection strategy — which visual tokens to include as "reference" — may affect performance on documents with unusual layouts
- Evaluation on OmniDocBench only; performance on other OCR benchmarks (DocVQA, TextVQA) not reported

---

## Source

- **Paper**: [arXiv:2606.23050](https://arxiv.org/abs/2606.23050)
- **Preprint date**: Jun 2026
