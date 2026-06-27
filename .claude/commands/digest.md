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
also writes a structured `inbox/digests/YYYY-MM-DD.json` (array of
`{n, source, id, title, url, snippet}`), and advances each source's
`last_seen.txt`.

For a preview without advancing pointers:
```bash
.venv/bin/python inbox/run_digest.py --dry-run
```

### 2. Prepare context for summarization

Read two files before spawning Haiku agents:

1. **The JSON sidecar** (`inbox/digests/YYYY-MM-DD.json`) — gives you the
   structured item list with ids and sources.
2. **The tag vocabulary** (`inbox/kb/tags.md`) — needed to embed in each
   Haiku prompt so tags are drawn from the controlled vocabulary.

Extract the single-line tag list from `tags.md` (the backtick-wrapped tokens
from bullet lines, e.g. `agents, robotics, rl, ...`).

### 3. Summarize each item with its own Haiku subagent

For each item from the JSON sidecar, spawn **one Haiku subagent per item**
(in parallel where possible):

```
Agent(
  model="haiku",
  prompt="""Summarize this item for a personal wiki on local AI and open-weight models.

Write:
1. A 2-3 sentence summary.
2. A one-line verdict (choose one):
   - Wiki-relevant — open-weight model, local inference tool, research paper, engineering technique
   - Minor — tangentially related, probably not worth a full wiki page
   - Skip — proprietary/API-only, AI policy/news, opinion, hype
3. A structured classification block (REQUIRED, output exactly this format):

```json
{
  "relevance": "wiki-relevant",
  "score": 4,
  "tags": ["agents", "rl"]
}
```

Rules for the classification block:
- relevance: must be exactly "wiki-relevant", "minor", or "skip"
- score: integer 0-5 (wiki-relevant → 4-5, minor → 2-3, skip → 0-1)
- tags: 2-5 tags chosen from this vocabulary:
  <TAG_VOCABULARY>
  Propose at most one new tag with a "?" prefix if nothing fits.

Item:
Title: <title>
URL: <url>
Snippet: <snippet>
"""
)
```

Replace `<TAG_VOCABULARY>` with the comma-separated tag list from step 2.
Spawn all per-item agents in parallel (one `Agent` call per item in a single
message) to keep the total wall time low.

### 4. File all items into the knowledge base (Stage D)

For each item, parse the Haiku agent's output to extract:
- The summary (the 2-3 sentence prose)
- The verdict (the one-line verdict)
- The JSON classification block (`relevance`, `score`, `tags`)

Then construct a JSON record and pipe it to `kb.py file`:

```bash
echo '<JSON_RECORD>' | .venv/bin/python inbox/kb/kb.py file --filed YYYY-MM-DD
```

Where `<JSON_RECORD>` is:
```json
{
  "id": "<item id from sidecar>",
  "title": "<title>",
  "url": "<url>",
  "source": "<source from sidecar>",
  "digest": "<today YYYY-MM-DD>",
  "relevance": "<from Haiku>",
  "score": <from Haiku>,
  "tags": [<from Haiku>],
  "summary": "<2-3 sentence summary from Haiku>",
  "verdict": "<one-line verdict from Haiku>"
}
```

Do this for **all items** regardless of relevance verdict — the KB stores
everything, including Minor and Skip items.

### 5. Reindex the knowledge base (Stage E)

After all items are filed:

```bash
.venv/bin/python inbox/kb/kb.py reindex
```

### 6. Present the digest to the user

Group by source. For each item show: number, title, URL, Haiku summary, verdict.

End with:

> Reply with item numbers to add any to the wiki.

### 7. Research items on request

When the user replies with numbers, for each selected item:

1. **Generate a stub** using the KB record as the starting point:
   ```bash
   .venv/bin/python inbox/kb/kb.py promote-stub <id> --section <section> --dry-run
   ```
   Use this stub as the scaffold for the wiki page.

2. **Research** to flesh out the stub:
   - Find arXiv ID if it's a paper: `WebSearch(allowed_domains=["arxiv.org"])`
   - Fetch content (arXiv abstract, GitHub README, or article URL)

3. **Decide section**: models / tools / research / software-thoughts

4. **Write the wiki page** (flesh out the stub with real content):
   - TL;DR block at the top
   - Source line with arXiv / GitHub / blog URL
   - Sections: problem, how it works, benchmarks, usage, limitations
   - Cross-links to related wiki pages

5. **Update nav and section index**:
   - Add to the correct section in `mkdocs.yml`
   - Add a row to `docs/<section>/index.md`

6. **Promote in KB** (without `--dry-run`) then **commit both** (wiki page +
   KB item update) together:
   ```bash
   .venv/bin/python inbox/kb/kb.py promote-stub <id> --section <section>
   git add docs/<section>/<slug>.md inbox/kb/items/<path>.md mkdocs.yml docs/<section>/index.md
   git commit -m "<section>: <short description>

   Co-Authored-By: AI"
   ```

## Notes

- Digests are written to `inbox/digests/` (gitignored — not committed).
- KB item files are written to `inbox/kb/items/` (committed to git).
- Twitter items come from `inbox/sources/twitter-follows/pending.json`,
  populated via `/project:add-tweet`.
- Reddit r/LocalLLaMA returns 403 from datacenter IPs — expected, handled
  gracefully by the orchestrator.
- Use `kb.py query --tag <tag>` to browse past items by topic.
- Use `kb.py related <id>` to find items sharing tags with a given item.
