# Add Source

Guide the creation of a new digest inbox datasource under `inbox/sources/`. Each
source is uniform: a directory with `source.md`, `last_seen.txt`, `enumerate.py`,
and `fetch.py`, following the contracts described below.

Invoked as `/project:add-source`.

## Gather the inputs from the user — do NOT guess

Ask the user for (or derive from the URL where unambiguous):

1. **Source ID** — a short kebab-case slug for the directory name (e.g.
   `arxiv-cs-cl`). Derive a suggestion from the URL host, but confirm.
2. **Name** — human-readable name.
3. **URL** — the page/feed/API endpoint.
4. **Type** — one of `rss` (Atom/RSS feed), `html` (scrape a page), or `api`
   (JSON API).
5. **Interest profile** — **ASK the user explicitly.** Do not invent it. This is
   the description of which items from this source are wiki-worthy vs skippable.
   The wiki covers open-weight model releases, local inference tools, training/
   inference research papers, and practical AI-engineering tips; it skips
   proprietary/API-only news, hype, and financial news — but the *source-specific*
   profile (what to keep vs skip from THIS source) must come from the user.

## Create the directory and files

Create `inbox/sources/<source-id>/` with all four files.

### `source.md`

Human + machine readable. Include: Name, URL (and Feed URL if rss), Type,
Description, the `last_seen.txt` pointer-format docs, the `fetch.py` argument
format, and the **Interest profile** the user gave you. Mirror the structure of
the existing `inbox/sources/*/source.md` files.

### `last_seen.txt`

One line, in whatever opaque format `enumerate.py` understands. Pick by type:
- `rss` → ISO 8601 datetime of the newest entry (start with a recent date).
- `html` (date-paged) → ISO date `YYYY-MM-DD`.
- `api` → whatever cursor the API uses (timestamp, ID, etc.).

### `enumerate.py`

Reads `last_seen.txt`, fetches new items, prints a JSON array to stdout, and —
only after successfully printing — advances `last_seen.txt`. Must accept a
`--dry-run` flag that skips the pointer update. stdout contract:

```json
[{"id": "string", "title": "string", "url": "string", "snippet": "string (~200 chars)"}]
```

Print `[]` when nothing is new. Use the shared helpers — they already implement
the common shapes:

- **rss** → wrap `lib.feed.enumerate_feed(FEED_URL, LAST_SEEN, dry_run)`. See
  `inbox/sources/simon-willison/enumerate.py` for the 15-line wrapper to copy.
- **html** → fetch with `lib.http.get(...)`, parse entries, dedupe, advance the
  pointer. Model it on `inbox/sources/huggingface-papers/enumerate.py`.
- **api** → fetch JSON with `lib.http.get(url, accept="application/json")`,
  filter by the cursor, advance. Model it on
  `inbox/sources/reddit-localllama/enumerate.py`.

All HTTP must go through `lib.http` (sets the `ai-local-digest/1.0` User-Agent).
Add `sys.path.insert(0, str(Path(__file__).resolve().parents[2]))` then
`from lib import ...` at the top, as the existing sources do.

### `fetch.py`

Takes the item id as `argv[1]`, fetches the full item content, prints plain text
to stdout. For `rss`/`html` sources, reuse `lib.webpage.fetch_text(url)`
(see `inbox/sources/simon-willison/fetch.py`). For `api` sources, fetch and
extract the relevant fields (see `inbox/sources/reddit-localllama/fetch.py`).

## Verify

Run the new source end to end before finishing:

```bash
.venv/bin/python inbox/sources/<source-id>/enumerate.py --dry-run
```

Confirm it prints a valid JSON array. If items come back, pick one id and run
`.venv/bin/python inbox/sources/<source-id>/fetch.py <id>` to confirm it returns text.

The new source is picked up automatically by `inbox/run_digest.py` (it globs
`inbox/sources/*/`). No registration needed.

## Notes

- Keep dependencies to `requests`, `feedparser`, `anthropic` (already in
  `inbox/requirements.txt`); prefer the standard library otherwise.
- Commit the new source directory including its initial `last_seen.txt`.
