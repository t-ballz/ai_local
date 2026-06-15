# huggingface-blog

- **Name:** Hugging Face Blog
- **URL:** https://huggingface.co/blog
- **Feed:** https://huggingface.co/blog/feed.xml
- **Type:** rss

## Description

The official Hugging Face blog. Carries model-release announcements, inference /
quantization deep-dives, fine-tuning guides, and ecosystem tooling posts —
often the primary source for open-weight model launches.

## Pointer format (`last_seen.txt`)

One line: an ISO 8601 datetime — the timestamp of the newest entry seen on the
last run. `enumerate.py` returns entries strictly newer than this and advances
the pointer to the newest entry seen.

## Pointer format (`fetch.py`)

`fetch.py` takes an entry URL as argv[1] and fetches the post page, extracting
the body text.

## Interest profile

Wiki-worthy items from this source:

- **Open-weight model releases** (new families, sizes, instruct/base variants).
- **Inference / quantization** posts: GGUF, bitsandbytes, GPTQ/AWQ, TGI, vLLM.
- **Fine-tuning / training** guides and method write-ups.
- **Local-inference** and on-device tooling.

Skip: pure HF product/platform marketing, hiring posts, event recaps, and
enterprise/API-only announcements without downloadable weights.
