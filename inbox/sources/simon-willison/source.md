# simon-willison

- **Name:** Simon Willison's Weblog (everything feed)
- **URL:** https://simonwillison.net/
- **Feed:** https://simonwillison.net/atom/everything/
- **Type:** rss (Atom)

## Description

Simon Willison writes prolifically about LLMs, local inference, prompt
engineering, and AI tooling — blog entries, link blogs, and quotations. His
"everything" Atom feed is a high-signal stream for practical AI engineering and
open-model news.

## Pointer format (`last_seen.txt`)

One line: an ISO 8601 datetime — the `updated`/`published` time of the newest
entry seen on the last run. `enumerate.py` returns entries strictly newer than
this, then advances the pointer to the newest entry timestamp seen.

## Pointer format (`fetch.py`)

`fetch.py` takes an entry URL as argv[1] and fetches the page, extracting the
post body text.

## Interest profile

Wiki-worthy items from this source:

- **Open-weight model releases** and hands-on notes about running them.
- **Local inference** tooling, CLI tricks, llm/llama.cpp/Ollama coverage.
- **Practical prompt-engineering and AI-engineering** tips.
- **Research-paper write-ups** relevant to training/inference.

Skip: pure project-release notes for unrelated software, conference logistics,
and proprietary/API-only product news without a local-inference angle.
