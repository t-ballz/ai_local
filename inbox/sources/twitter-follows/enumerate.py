#!/usr/bin/env python3
"""Enumerate Twitter items — always empty by design.

Twitter access here is pull-by-ID via FxEmbed, which has NO user-timeline
endpoint. There is no way to poll the followed accounts for new tweets, so this
enumerator cannot discover items on its own and always prints an empty array.

Tweets enter the digest manually through the `/project:add-tweet` skill, which
fetches a tweet by ID (fetch.py), summarizes it, and appends it to pending.json.
run_digest.py reads pending.json and surfaces those items under this source.

stdout contract: JSON array (always `[]` here).
"""
from __future__ import annotations

import sys


def main() -> int:
    # --dry-run is accepted for a uniform interface but is a no-op: this source
    # never advances last_seen.txt (nothing to enumerate).
    sys.stdout.write("[]\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
