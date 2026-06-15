#!/usr/bin/env python3
"""Fetch a single HF paper's abstract + metadata.

argv[1] is an arXiv ID (e.g. 2401.12345) or a full HF/arXiv paper URL.
Prints plain text (title + abstract) to stdout for summarization.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import http  # noqa: E402

BASE = "https://huggingface.co"


def extract_arxiv_id(arg: str) -> str:
    m = re.search(r"(\d{4}\.\d{4,5})", arg)
    return m.group(1) if m else arg.strip()


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_arxiv_abstract(arxiv_id: str) -> str:
    """Pull the abstract from the static arXiv abstract page. '' on failure."""
    try:
        resp = http.get(f"https://arxiv.org/abs/{arxiv_id}")
    except Exception:  # noqa: BLE001
        return ""
    m = re.search(
        r'<blockquote class="abstract[^"]*">(.*?)</blockquote>',
        resp.text,
        re.DOTALL,
    )
    if not m:
        return ""
    text = strip_html(m.group(1))
    # arXiv prefixes the block with "Abstract:" — drop the redundant label.
    return re.sub(r"^Abstract:\s*", "", text, flags=re.IGNORECASE)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch.py <arxiv-id-or-url>", file=sys.stderr)
        return 2

    arxiv_id = extract_arxiv_id(sys.argv[1])
    url = f"{BASE}/papers/{arxiv_id}"
    resp = http.get(url)
    html = resp.text

    parts: list[str] = [f"arXiv: {arxiv_id}", url]

    # Title is usually the first <h1>.
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if h1:
        parts.append("Title: " + strip_html(h1.group(1)))

    # HF renders the abstract client-side, so the og:description meta is often a
    # generic placeholder. Pull the real abstract from the arXiv abstract page,
    # which is static. Fall back to the HF meta tag if arXiv is unreachable.
    abstract = fetch_arxiv_abstract(arxiv_id)
    if not abstract:
        meta = re.search(r'<meta[^>]+property="og:description"[^>]+content="([^"]+)"', html)
        if not meta:
            meta = re.search(r'<meta[^>]+name="description"[^>]+content="([^"]+)"', html)
        if meta:
            abstract = strip_html(meta.group(1))
    if abstract:
        parts.append("Abstract: " + abstract)

    print("\n\n".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
