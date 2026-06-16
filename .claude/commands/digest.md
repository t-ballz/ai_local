# Daily Digest

Generate and present the daily digest of new items from all configured inbox
sources (Hugging Face papers + blog, r/LocalLLaMA, Simon Willison, and pending
Twitter items).

## Steps

### 1. Run the digest orchestrator

```bash
.venv/bin/python inbox/run_digest.py
```

This enumerates every source under `inbox/sources/*/`, writes a raw markdown
listing (titles + snippets, no AI summaries) to `inbox/digests/YYYY-MM-DD.md`,
advances each source's `last_seen.txt`, and prints the same to stdout.

For a preview without advancing pointers:
```bash
.venv/bin/python inbox/run_digest.py --dry-run
```

### 2. Summarize with a Haiku subagent

Collect all items from the orchestrator output (title, URL, snippet). Spawn a
**single Haiku subagent** to process all items at once:

```
Agent(
  model="haiku",
  prompt="""You are a triage assistant for a personal wiki on local AI and open-weight models.

For each item below, write:
1. A 2-3 sentence summary of what it is.
2. A wiki-relevance verdict: Skip | Minor | Wiki-relevant

Wiki-relevant = open-weight model release, local inference tool, research paper
on training/architecture/agents, or practical AI-engineering technique.
Skip = proprietary/API-only, AI policy/news, non-AI topics.
Minor = tangentially related, probably not worth a full page.

Items:
<numbered list of title + URL + snippet>
"""
)
```

Use one agent call for all items — do not spawn one per item.

### 3. Present the digest to the user

Group by source. For each item show: number, title, URL, Haiku summary, verdict.

End with:

> Reply with item numbers to research any of these into the wiki.

### 4. Research items on request

When the user replies with numbers, research each using the workflow in
`/project:add-tweet`'s "research now" path:

1. Find arXiv ID if it's a paper: `WebSearch(allowed_domains=["arxiv.org"])`
2. Fetch content (arXiv abstract, GitHub README, or article URL)
3. Decide section: models / tools / research / software-thoughts
4. Write the wiki page
5. Update `mkdocs.yml` and the section's `index.md`
6. Commit

## Notes

- Digests are written to `inbox/digests/` (gitignored — not committed).
- Twitter items come from `inbox/sources/twitter-follows/pending.json`,
  populated via `/project:add-tweet`.
- Reddit r/LocalLLaMA returns 403 from datacenter IPs — expected, handled
  gracefully by the orchestrator.
