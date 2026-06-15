#!/usr/bin/env python3
"""Fetch a single r/LocalLLaMA post: title, selftext, and top comments.

argv[1] is the base-36 Reddit post ID (e.g. 1abc2de).
Prints plain text to stdout for summarization.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import http  # noqa: E402

MAX_COMMENTS = 5


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch.py <post-id>", file=sys.stderr)
        return 2

    post_id = sys.argv[1].strip()
    # strip a t3_ prefix if present
    if post_id.startswith("t3_"):
        post_id = post_id[3:]

    url = f"https://www.reddit.com/comments/{post_id}.json"
    resp = http.get(url, accept="application/json")
    data = resp.json()

    parts: list[str] = []

    # data[0] = post listing, data[1] = comment listing
    try:
        post = data[0]["data"]["children"][0]["data"]
        title = post.get("title", "")
        selftext = (post.get("selftext") or "").strip()
        link = post.get("url", "")
        if title:
            parts.append("Title: " + title)
        if link and link != url:
            parts.append("Link: " + link)
        if selftext:
            parts.append("Body:\n" + selftext)
    except (KeyError, IndexError, TypeError):
        pass

    try:
        comments = data[1]["data"]["children"]
        top: list[str] = []
        for c in comments:
            if c.get("kind") != "t1":
                continue
            body = (c.get("data", {}).get("body") or "").strip()
            if body:
                top.append(body)
            if len(top) >= MAX_COMMENTS:
                break
        if top:
            parts.append("Top comments:\n" + "\n---\n".join(top))
    except (KeyError, IndexError, TypeError):
        pass

    print("\n\n".join(parts) if parts else "(no content)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
