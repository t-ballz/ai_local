# Daily Digest

Generate and present the daily digest of new items from all configured inbox
sources (Hugging Face papers + blog, r/LocalLLaMA, Simon Willison, and pending
Twitter items).

## Steps

### 1. Run the digest orchestrator

```bash
.venv/bin/python inbox/run_digest.py
```

This enumerates every source under `inbox/sources/*/`, attempts Haiku summaries,
writes the result to `inbox/digests/YYYY-MM-DD.md`, and advances each source's
`last_seen.txt`.

**Note on Haiku summaries:** `ANTHROPIC_API_KEY` is not exposed to subprocesses
by Claude Code, so all summaries will show `(no Haiku summary — set ANTHROPIC_API_KEY)`.
This is expected. You will summarize items yourself in step 3.

For a preview without advancing pointers:
```bash
.venv/bin/python inbox/run_digest.py --dry-run
```

### 2. Read the digest file

```
inbox/digests/<today>.md
```

Note which items have content to summarize (items with a URL are fetchable).

### 3. Present the digest to the user

Group by source. For each item:
- **Number** it sequentially across all sources
- Show: **title**, **URL**, your **2-3 sentence summary** (fetch the URL if needed
  to write a meaningful summary), and a **wiki-relevance verdict**

For items where the title alone is enough to judge (opinion pieces, changelogs with
no local-AI angle): summarize from the title + snippet without fetching.

For items that look wiki-relevant: fetch the URL and summarize properly before
presenting.

**Wiki-relevance verdicts:**
- **Skip** — proprietary models, AI policy/news, non-AI topics
- **Minor** — tangentially relevant; probably not worth a full page
- **Wiki-relevant** — open-weight model, local tool, research paper, engineering technique

### 4. Offer research

End with:

> Reply with item numbers to research any of these into the wiki.

When the user replies with numbers, research each item using the same workflow as
`/project:add-tweet`'s "research now" path:

1. Find arXiv ID if it's a paper (`WebSearch` with `allowed_domains=["arxiv.org"]`)
2. Fetch content (arXiv abstract, GitHub README, or article)
3. Decide section (models / tools / research / software-thoughts)
4. Write the wiki page
5. Update `mkdocs.yml` and the section's `index.md`
6. Commit

## Notes

- Digests are written to `inbox/digests/` (gitignored — not committed).
- Twitter items come from `inbox/sources/twitter-follows/pending.json`,
  populated via `/project:add-tweet`.
- Reddit r/LocalLLaMA returns 403 from datacenter IPs — this is expected and
  handled gracefully; the orchestrator logs the error and continues.
