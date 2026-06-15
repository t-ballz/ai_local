#!/usr/bin/env python3
"""Enumerate new top r/LocalLLaMA posts since last_seen.

last_seen.txt holds a Unix timestamp (the newest created_utc seen last run).
We fetch the top-of-day listing, keep posts strictly newer than that, emit them
as JSON, then advance the pointer to the newest created_utc seen.

stdout contract: JSON array of {id, title, url, snippet}.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import http  # noqa: E402

HERE = Path(__file__).resolve().parent
LAST_SEEN = HERE / "last_seen.txt"
LISTING = "https://www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=25"
MAX_ITEMS = 25


def read_last_seen() -> float:
    try:
        return float(LAST_SEEN.read_text().strip())
    except Exception:  # noqa: BLE001
        return 0.0


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]
    last = read_last_seen()

    resp = http.get(LISTING, accept="application/json")
    data = resp.json()
    children = data.get("data", {}).get("children", [])

    items: list[dict] = []
    newest = last
    for child in children:
        post = child.get("data", {})
        created = float(post.get("created_utc", 0))
        if created <= last:
            continue
        newest = max(newest, created)
        post_id = post.get("id", "")
        title = post.get("title", "(no title)")
        permalink = post.get("permalink", "")
        url = f"https://www.reddit.com{permalink}" if permalink else post.get("url", "")
        selftext = (post.get("selftext") or "").strip()
        snippet = (selftext or title)[:200]
        items.append(
            {
                "id": post_id,
                "title": title,
                "url": url,
                "snippet": snippet,
            }
        )

    if len(items) > MAX_ITEMS:
        skipped = len(items) - MAX_ITEMS
        items = items[:MAX_ITEMS]
        print(
            f"CAP_WARNING: showing {MAX_ITEMS} of {MAX_ITEMS + skipped} new items "
            f"({skipped} more not shown — increase MAX_ITEMS or run again to advance pointer)",
            file=sys.stderr,
        )

    sys.stdout.write(json.dumps(items) + "\n")
    sys.stdout.flush()

    if not dry_run and newest > last:
        LAST_SEEN.write_text(str(int(newest)) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
