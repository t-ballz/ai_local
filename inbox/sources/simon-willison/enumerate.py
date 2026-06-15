#!/usr/bin/env python3
"""Enumerate new entries from Simon Willison's Atom feed.

Thin wrapper over lib.feed.enumerate_feed. last_seen.txt holds the ISO datetime
of the newest entry seen last run.

stdout contract: JSON array of {id, title, url, snippet}.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import feed  # noqa: E402

HERE = Path(__file__).resolve().parent
LAST_SEEN = HERE / "last_seen.txt"
FEED_URL = "https://simonwillison.net/atom/everything/"


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]
    return feed.enumerate_feed(FEED_URL, LAST_SEEN, dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
