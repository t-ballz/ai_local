#!/usr/bin/env python3
"""Fetch the body text of a Hugging Face blog post.

argv[1] is the entry URL. Prints plain text to stdout for summarization.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib import webpage  # noqa: E402


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fetch.py <entry-url>", file=sys.stderr)
        return 2
    print(webpage.fetch_text(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
