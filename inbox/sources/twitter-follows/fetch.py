#!/usr/bin/env python3
"""Fetch a single tweet via the FxEmbed API.

argv[1] is a tweet ID (numeric snowflake) or a tweet URL from x.com /
twitter.com / fixupx.com / fxtwitter.com / vxtwitter.com (the screen_name in the
path is ignored — only the ID matters).

Prints plain text (author + tweet text + metadata) to stdout for summarization.

API: https://api.fxtwitter.com/2/status/{tweet_id}  (no key, ~1000 req/min)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import http  # noqa: E402

API = "https://api.fxtwitter.com/2/status/{id}"


def extract_id(arg: str) -> str:
    arg = arg.strip()
    # URL form: .../status/<id>(?query)
    m = re.search(r"/status/(\d+)", arg)
    if m:
        return m.group(1)
    # Bare numeric ID
    m = re.search(r"(\d{6,})", arg)
    return m.group(1) if m else arg


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch.py <tweet-id-or-url>", file=sys.stderr)
        return 2

    tweet_id = extract_id(sys.argv[1])
    resp = http.get(API.format(id=tweet_id), accept="application/json")
    data = resp.json()

    if data.get("code") != 200:
        print(f"(fxtwitter error {data.get('code')}: {data.get('message')})")
        return 0

    s = data.get("status", {})
    author = s.get("author", {})
    parts: list[str] = []
    handle = author.get("screen_name", "")
    name = author.get("name", "")
    parts.append(f"Tweet by {name} (@{handle})")
    if s.get("url"):
        parts.append(s["url"])
    if s.get("created_at"):
        parts.append("Posted: " + s["created_at"])
    parts.append("")
    parts.append(s.get("text", ""))

    # Include quoted tweet text if present — often carries the substance.
    quote = s.get("quote")
    if quote and quote.get("text"):
        q_author = quote.get("author", {}).get("screen_name", "")
        parts.append("")
        parts.append(f"Quoting @{q_author}: {quote['text']}")

    # Thread context if FxEmbed returned it.
    thread = data.get("thread")
    if isinstance(thread, list) and thread:
        parts.append("")
        parts.append("Thread context:")
        for t in thread:
            if isinstance(t, dict) and t.get("text"):
                parts.append("- " + t["text"])

    print("\n".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
