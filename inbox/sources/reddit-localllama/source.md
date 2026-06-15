# reddit-localllama

- **Name:** r/LocalLLaMA (top of day)
- **URL:** https://www.reddit.com/r/LocalLLaMA
- **Type:** api (Reddit public JSON, no auth)

## Description

The r/LocalLLaMA subreddit is the community hub for running open-weight LLMs
locally. The digest polls the "top of the day" listing for the most-upvoted
posts: model releases, quantization tricks, hardware/benchmark threads, and
tooling announcements.

Enumeration endpoint:
`https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=25`

## Pointer format (`last_seen.txt`)

One line: a Unix timestamp integer — the `created_utc` of the newest post seen
on the last run. `enumerate.py` returns posts strictly newer than this and then
advances the pointer to the newest `created_utc` it saw.

## Pointer format (`fetch.py`)

`fetch.py` takes a Reddit post ID (the base-36 `id`, e.g. `1abc2de`) as argv[1]
and fetches `https://www.reddit.com/comments/{id}.json` for the title, selftext,
and a few top comments.

## Interest profile

Wiki-worthy items from this source:

- **New open-weight model releases** and weight drops (HF/GGUF links).
- **Local inference tooling**: llama.cpp / Ollama / LM Studio / vLLM updates,
  new quant formats, KV-cache tricks.
- **Hardware + benchmark** posts that inform local-inference hardware notes.
- **Practical how-tos** for running models locally.

Skip: meme/discussion threads with no concrete artifact, "which model should I
use" help requests, drama, and proprietary/API-only model news.
