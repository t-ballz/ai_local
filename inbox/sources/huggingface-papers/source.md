# huggingface-papers

- **Name:** Hugging Face Papers (Daily Papers)
- **URL:** https://huggingface.co/papers
- **Type:** html

## Description

Hugging Face's curated daily papers page. Surfaces trending arXiv papers the ML
community is discussing, each with a title, authors, and an arXiv ID. Good early
signal for influential training / inference / model-release papers.

## Pointer format (`last_seen.txt`)

One line: an ISO date `YYYY-MM-DD`. It records the date the digest last ran.
`enumerate.py` returns papers whose listing date is strictly after this value,
then writes today's date back.

Because the HF papers page is organized by date, enumeration walks the dated
pages (`https://huggingface.co/papers/date/YYYY-MM-DD`) from the day after
`last_seen` up to today.

## Pointer format (`fetch.py`)

`fetch.py` takes an arXiv ID (e.g. `2401.12345`) or a full paper URL as argv[1]
and fetches that paper's HF page for the abstract and metadata.

## Interest profile

Wiki-worthy items from this source:

- Papers introducing or evaluating **open-weight models** (weights downloadable).
- Papers on **training methods, fine-tuning, RLHF/RL, distillation**.
- Papers on **inference efficiency**: quantization, KV-cache, speculative decoding,
  MoE serving, long-context.
- Papers on **local / on-device inference** and small-model capability.

Skip: papers that are purely about closed/proprietary systems, pure theory with no
open artifacts, or unrelated ML subfields (e.g. robotics control, pure CV detection)
unless they bear on local LLM inference.
