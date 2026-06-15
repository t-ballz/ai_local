# Daily Digest

Generate and present the daily digest of new items from all configured inbox
sources (Hugging Face papers + blog, r/LocalLLaMA, Simon Willison, and pending
Twitter items).

## Steps

1. Run the digest orchestrator:

   ```bash
   .venv/bin/python inbox/run_digest.py
   ```

   This enumerates every source under `inbox/sources/*/`, fetches and
   Haiku-summarizes each new item, writes the result to
   `inbox/digests/YYYY-MM-DD.md`, and prints it to stdout. It advances each
   source's `last_seen.txt`, so re-running later the same day will show only
   items new since this run.

   - If you only want a preview without advancing the pointers, run
     `.venv/bin/python inbox/run_digest.py --dry-run` instead.

2. Read the written digest file (`inbox/digests/<today>.md`) to confirm the
   contents.

3. Present the digest to the user in the conversation, grouped by source, with a
   numbered list. For each item show: the number, title, URL, the 2-3 sentence
   summary, and the wiki-relevance verdict line.

4. End with this offer:

   > Reply with item numbers to research any of these into the wiki.

   When the user replies with numbers, treat each as a request to research that
   item into the wiki following the normal task-based workflow in `AGENTS.md`
   (create a `tasks/NNNN-slug.md`, then process it). Use the item's URL and, if
   helpful, re-run the source's `fetch.py {id}` to pull full content.

## Notes

- This is invocable as `/project:digest`.
- The digest is written under `inbox/digests/`, which is gitignored — it is
  ephemeral run output, not committed.
- Twitter items shown come from `inbox/sources/twitter-follows/pending.json`,
  populated via `/project:add-tweet`.
