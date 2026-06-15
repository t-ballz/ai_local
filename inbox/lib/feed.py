"""Shared Atom/RSS enumeration for feed-based sources.

simon-willison and huggingface-blog are the same shape: an Atom/RSS feed plus a
last_seen.txt holding the ISO datetime of the newest entry processed. This helper
implements that pattern so each source's enumerate.py is a thin wrapper.

Uses feedparser when available; otherwise falls back to stdlib XML parsing.
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

from lib import http


def _parse_dt(value: str) -> datetime.datetime | None:
    if not value:
        return None
    value = value.strip()
    # Try ISO 8601 first (handles the values we write back).
    try:
        dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
        return _aware(dt)
    except ValueError:
        pass
    # RFC 822 (RSS pubDate) and RFC 3339 via email.utils.
    try:
        from email.utils import parsedate_to_datetime

        dt = parsedate_to_datetime(value)
        return _aware(dt) if dt else None
    except (TypeError, ValueError):
        return None


def _aware(dt: datetime.datetime) -> datetime.datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def _entries_feedparser(raw: bytes) -> list[dict]:
    import feedparser

    parsed = feedparser.parse(raw)
    out: list[dict] = []
    for e in parsed.entries:
        when = (
            e.get("updated")
            or e.get("published")
            or e.get("created")
            or ""
        )
        summary = e.get("summary", "") or ""
        out.append(
            {
                "id": e.get("id") or e.get("link", ""),
                "title": e.get("title", "(untitled)"),
                "url": e.get("link", ""),
                "when": when,
                "summary": summary,
            }
        )
    return out


def _entries_stdlib(raw: bytes) -> list[dict]:
    """Minimal Atom+RSS parser fallback when feedparser is unavailable."""
    import xml.etree.ElementTree as ET

    root = ET.fromstring(raw)
    out: list[dict] = []

    def text(el, *names):
        for n in names:
            found = el.find(n)
            if found is not None and found.text:
                return found.text
        return ""

    # Atom: <entry> under namespace; RSS: <item> under <channel>.
    atom_ns = "{http://www.w3.org/2005/Atom}"
    for entry in root.iter(f"{atom_ns}entry"):
        link_el = entry.find(f"{atom_ns}link")
        link = link_el.get("href") if link_el is not None else ""
        out.append(
            {
                "id": text(entry, f"{atom_ns}id") or link,
                "title": text(entry, f"{atom_ns}title") or "(untitled)",
                "url": link,
                "when": text(entry, f"{atom_ns}updated", f"{atom_ns}published"),
                "summary": text(entry, f"{atom_ns}summary", f"{atom_ns}content"),
            }
        )
    if out:
        return out
    # RSS fallback
    for item in root.iter("item"):
        out.append(
            {
                "id": text(item, "guid", "link"),
                "title": text(item, "title") or "(untitled)",
                "url": text(item, "link"),
                "when": text(item, "pubDate"),
                "summary": text(item, "description"),
            }
        )
    return out


def enumerate_feed(feed_url: str, last_seen_path: Path, dry_run: bool) -> int:
    """Run the shared feed enumeration and write the JSON contract to stdout."""
    last_raw = last_seen_path.read_text().strip() if last_seen_path.exists() else ""
    last_dt = _parse_dt(last_raw)

    resp = http.get(feed_url)
    raw = resp.content
    try:
        entries = _entries_feedparser(raw)
    except ImportError:
        entries = _entries_stdlib(raw)

    items: list[dict] = []
    newest = last_dt
    for e in entries:
        when = _parse_dt(e["when"])
        if last_dt is not None and when is not None and when <= last_dt:
            continue
        if when is not None and (newest is None or when > newest):
            newest = when
        summary = e["summary"]
        items.append(
            {
                "id": e["url"] or e["id"],
                "title": e["title"],
                "url": e["url"],
                "snippet": summary[:200],
            }
        )

    sys.stdout.write(json.dumps(items) + "\n")
    sys.stdout.flush()

    if not dry_run and newest is not None and newest != last_dt:
        last_seen_path.write_text(newest.isoformat() + "\n")

    return 0
