#!/usr/bin/env python3
"""Enumerate new Hugging Face daily papers since last_seen.

last_seen.txt holds an ISO date. We walk the dated papers pages from the day
after last_seen up to today, extract paper entries, and emit them as a JSON
array.

If the number of new items exceeds MAX_ITEMS, we emit the first MAX_ITEMS,
save a skip count to offset.txt, and do NOT advance last_seen. The next run
re-fetches the same date range, skips the already-emitted items, and shows
the next batch. last_seen only advances once the backlog is fully consumed.

stdout contract: JSON array of {id, title, url, snippet}.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import http  # noqa: E402

HERE = Path(__file__).resolve().parent
LAST_SEEN = HERE / "last_seen.txt"
OFFSET_FILE = HERE / "offset.txt"
BASE = "https://huggingface.co"
MAX_ITEMS = 20


def read_last_seen() -> datetime.date:
    raw = LAST_SEEN.read_text().strip()
    return datetime.date.fromisoformat(raw)


def read_offset() -> int:
    if OFFSET_FILE.exists():
        try:
            return int(OFFSET_FILE.read_text().strip())
        except ValueError:
            return 0
    return 0


def daterange(start: datetime.date, end: datetime.date):
    """Yield dates in (start, end] — i.e. day after last_seen through today."""
    d = start + datetime.timedelta(days=1)
    while d <= end:
        yield d
        d += datetime.timedelta(days=1)


def parse_papers(html: str) -> list[dict]:
    """Extract paper entries from a HF papers HTML page.

    HF renders paper links as /papers/<arxiv_id>. We collect unique arxiv IDs
    and pull the nearest title text. This is intentionally tolerant: HF markup
    changes, so we rely only on the stable /papers/<id> link pattern.
    """
    items: list[dict] = []
    seen: set[str] = set()
    # Match anchors pointing at /papers/<arxiv-id>, capturing the link text.
    pattern = re.compile(
        r'<a[^>]+href="/papers/(\d{4}\.\d{4,5})"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    for m in pattern.finditer(html):
        arxiv_id = m.group(1)
        if arxiv_id in seen:
            continue
        title = re.sub(r"<[^>]+>", "", m.group(2))
        title = re.sub(r"\s+", " ", title).strip()
        if not title:
            continue
        seen.add(arxiv_id)
        items.append(
            {
                "id": arxiv_id,
                "title": title,
                "url": f"{BASE}/papers/{arxiv_id}",
                "snippet": title[:200],
            }
        )
    return items


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]
    last = read_last_seen()
    offset = read_offset()
    today = datetime.date.today()

    all_items: list[dict] = []
    seen_ids: set[str] = set()
    for day in daterange(last, today):
        url = f"{BASE}/papers/date/{day.isoformat()}"
        try:
            resp = http.get(url)
        except Exception:  # noqa: BLE001 - a missing/failed day shouldn't abort
            continue
        for it in parse_papers(resp.text):
            if it["id"] not in seen_ids:
                seen_ids.add(it["id"])
                all_items.append(it)

    # Skip items already shown in previous capped runs.
    remaining = all_items[offset:]
    total_remaining = len(remaining)

    if total_remaining > MAX_ITEMS:
        skipped = total_remaining - MAX_ITEMS
        items = remaining[:MAX_ITEMS]
        print(
            f"CAP_WARNING: showing {MAX_ITEMS} of {total_remaining} new items "
            f"({skipped} more — run again to continue)",
            file=sys.stderr,
        )
    else:
        items = remaining

    # Print first so a crash mid-write can't advance the pointer.
    sys.stdout.write(json.dumps(items) + "\n")
    sys.stdout.flush()

    if not dry_run:
        if total_remaining > MAX_ITEMS:
            # Backlog remains: save new offset, keep last_seen unchanged.
            OFFSET_FILE.write_text(str(offset + MAX_ITEMS) + "\n")
        else:
            # Backlog cleared: advance last_seen, remove offset file.
            LAST_SEEN.write_text(today.isoformat() + "\n")
            if OFFSET_FILE.exists():
                OFFSET_FILE.unlink()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
