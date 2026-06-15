"""Fetch a web page and extract readable body text.

Used by feed-based sources' fetch.py to turn an entry URL into plain text for
summarization. Heuristic, dependency-free: strips script/style, prefers <article>
or <main> content, then falls back to the whole body.
"""
from __future__ import annotations

import html as html_lib
import re

from lib import http


def extract_text(html: str) -> str:
    # Drop scripts and styles entirely.
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.DOTALL | re.IGNORECASE)

    # Prefer the main article region if present.
    region = None
    for tag in ("article", "main"):
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, re.DOTALL | re.IGNORECASE)
        if m:
            region = m.group(1)
            break
    if region is None:
        body = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
        region = body.group(1) if body else html

    text = re.sub(r"<[^>]+>", " ", region)
    text = html_lib.unescape(text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def fetch_text(url: str) -> str:
    resp = http.get(url)
    return extract_text(resp.text)
