# Add Tweet

Manually intake a single X/Twitter post into the digest inbox. Use this when the
user provides a tweet URL or ID — the `twitter-follows` source cannot poll
timelines (FxEmbed is pull-by-ID only), so tweets enter the system here.

Invoked as `/project:add-tweet <fixupx-url-or-tweet-id>`.

## Input

`$ARGUMENTS` is the tweet URL or numeric ID. Accept any of:
`x.com`, `twitter.com`, `fixupx.com`, `fxtwitter.com`, `vxtwitter.com` URLs, or a
bare tweet ID. `fetch.py` extracts the ID itself, so pass the argument through.

## Steps

1. Fetch the tweet:

   ```bash
   python inbox/sources/twitter-follows/fetch.py "<url-or-id>"
   ```

2. Summarize it (pipe the fetched content into the shared summarizer):

   ```bash
   python inbox/sources/twitter-follows/fetch.py "<url-or-id>" | python inbox/lib/summarize.py
   ```

3. Show the user the tweet author/text, the 2-3 sentence summary, and the
   wiki-relevance verdict line.

4. If the verdict is **Skip**, say so and stop (don't save). If it is
   **Wiki-relevant**, ask:

   > Research this into the wiki now, or save to inbox for later?

5. **If saving for later:** append an entry to
   `inbox/sources/twitter-follows/pending.json`. The file is a JSON array;
   append an object of the form:

   ```json
   {
     "id": "<tweet-id>",
     "url": "<canonical tweet url, e.g. https://x.com/<handle>/status/<id>>",
     "title": "<short title, e.g. 'Tweet by @handle: first words…'>",
     "snippet": "<first ~200 chars of the tweet text>",
     "summary": "<the full summary + wiki-relevance line from step 2>"
   }
   ```

   Read the existing array, append, and write it back as valid JSON (do not
   clobber existing entries). These items then appear under `twitter-follows` in
   the next `/project:digest`.

6. **If researching now:** follow the task-based workflow in `AGENTS.md` —
   create a `tasks/NNNN-slug.md` for the wiki page and process it. Use the tweet
   content (and any links it references) as source material.

## Notes

- No API key is needed for FxEmbed.
- Get the canonical `id`/`url` from the `fetch.py` output (it prints the tweet's
  `url`), or from the input URL.
