# twitter-follows

- **Name:** X/Twitter follows (curated AI/ML accounts)
- **URL:** https://x.com/
- **Type:** api (FxEmbed, single-tweet fetch by ID)

## Followed accounts

These are the X/Twitter accounts followed for wiki content:

- `@gntalktalk`
- `@xeophon`
- `@howtoprompt__`
- `@oliviacoder1`
- `@suraj_sharma14`
- `@che_shr_cat`
- `@_avichawla`

## Access / API

Tweets are fetched via the FxEmbed public API (no key required):

```
https://api.fxtwitter.com/2/status/{tweet_id}
```

This is a **single-tweet fetch by ID** — FxEmbed has **no user-timeline
endpoint**, so there is no way to poll an account for new tweets programmatically.

## Why enumeration is manual

Because Twitter access here is pull-by-ID, this source cannot poll accounts for
new items. Its `enumerate.py` therefore always prints `[]`. Tweets enter the
digest via the **`/project:add-tweet`** skill, which:

1. Fetches the tweet by ID via `fetch.py`.
2. Summarizes it with `lib/summarize.py`.
3. On approval, appends an entry to `pending.json` in this directory.

`run_digest.py` reads `pending.json` and shows those pending tweets under this
source in the digest.

## Pointer format (`last_seen.txt`)

A JSON object mapping handle → last tweet ID seen. It is **not** used for
polling (there is no timeline endpoint); it exists so a future timeline-capable
backend could resume per-account. Initialized to `0` per handle.

## Pointer format (`fetch.py`)

`fetch.py` takes a tweet ID (or a fixupx/x.com/twitter.com URL) as argv[1] and
fetches the tweet text + author + metadata via FxEmbed.

## Pending file (`pending.json`)

A JSON array of `{id, url, title, snippet, summary}` objects appended by the
`add-tweet` skill. Cleared manually after items are researched into the wiki.

## Interest profile

Wiki-worthy items from this source:

- **Open-weight model release** announcements / benchmarks from these accounts.
- **Local inference** tips, tooling, and quantization notes.
- **Practical prompt / AI-engineering** threads.
- **Research-paper** pointers relevant to training/inference.

Skip: personal/social chatter, proprietary-model hype, reposts without added
substance, and engagement-bait threads.
