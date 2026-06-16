# Add Tweet

Manually intake a single X/Twitter post into the digest inbox. Use this when the
user provides a tweet URL or ID — the `twitter-follows` source cannot poll
timelines (FxEmbed is pull-by-ID only), so tweets enter the system here.

Invoked as `/project:add-tweet <url-or-id>`.

## Input

`$ARGUMENTS` is the tweet URL or numeric ID. Accept any of:
`x.com`, `twitter.com`, `fixupx.com`, `fxtwitter.com`, `vxtwitter.com` URLs, or a
bare tweet ID. `fetch.py` extracts the ID itself, so pass the argument through.

## Steps

### 1. Fetch the tweet

```bash
.venv/bin/python inbox/sources/twitter-follows/fetch.py "<url-or-id>"
```

### 2. Assess the tweet yourself

**Do not run `summarize.py`** — `ANTHROPIC_API_KEY` is not exposed to subprocesses
by Claude Code, so it always returns the fallback string. Summarize from the fetched
content directly.

Write a 2-3 sentence summary and a wiki-relevance verdict:

- **Skip** — opinion, hype, proprietary/API-only tools, news without a concrete
  artifact (model weights, paper, open-source tool).
- **Wiki-relevant** — open-weight model release, local inference tool, research
  paper, practical engineering technique.

### 3. Present to the user

Show: tweet author/handle, tweet text, your summary, and the verdict.

If **Skip**: say so and stop.

If **Wiki-relevant**, ask:

> Research this into the wiki now, or save to inbox for later?

### 4a. Save for later

Append to `inbox/sources/twitter-follows/pending.json` (read → append → write,
never clobber):

```json
{
  "id": "<tweet-id>",
  "url": "https://x.com/<handle>/status/<id>",
  "title": "<short title, e.g. 'Tweet by @handle: first words…'>",
  "snippet": "<first ~200 chars of tweet text>",
  "summary": "<your 2-3 sentence summary + verdict>"
}
```

### 4b. Research now

Follow this workflow:

**If the tweet references a research paper:**

1. Find the arXiv ID using a targeted search:
   ```
   WebSearch(query="<paper title or key terms>", allowed_domains=["arxiv.org"])
   ```
2. Fetch the abstract for full details:
   ```
   WebFetch("https://arxiv.org/abs/<id>", prompt="Extract: ...")
   ```
3. Fetch the GitHub repo README if one is linked.

**Decide where to file it:**

| Content type | Section |
|-------------|---------|
| Open-weight model family or variant | `docs/models/` |
| Specialised model (ASR, TTS, embedding, image) | `docs/models/` → Specialized |
| Local inference tool / RAG / code intelligence | `docs/tools/` |
| Research paper (training, architecture, agents) | `docs/research/` |
| Foundational software engineering concept | `docs/software-thoughts/` |

**Write the wiki page**, following the style of existing pages in the same section:
- TL;DR block at the top
- Source line with arXiv / GitHub / blog URL
- Sections covering: the problem, how it works, benchmarks, usage (if a tool), limitations
- Cross-links to related wiki pages where relevant

**Update the nav and section index:**
- Add the page to the correct section in `mkdocs.yml`
- Add a row to `docs/<section>/index.md`

**Commit:**
```bash
git add <files> && git commit -m "<section>: <short description>

Co-Authored-By: AI"
```

## Notes

- No API key is needed for FxEmbed.
- The canonical tweet URL and ID are printed by `fetch.py`.
