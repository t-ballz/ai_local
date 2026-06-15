"""Shared HTTP helper for the digest inbox sources.

All network access for the inbox goes through here so the User-Agent and
timeout policy stay consistent across sources.
"""
from __future__ import annotations

import requests

USER_AGENT = "ai-local-digest/1.0"
DEFAULT_TIMEOUT = 30


def get(url: str, *, accept: str | None = None, timeout: int = DEFAULT_TIMEOUT) -> requests.Response:
    """GET a URL with the standard digest User-Agent. Raises on HTTP error."""
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp
