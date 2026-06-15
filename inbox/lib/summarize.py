#!/usr/bin/env python3
"""Summarize an inbox item with Haiku for the daily digest.

Reads item content from stdin, calls Claude Haiku via the anthropic library,
and prints a 2-3 sentence summary plus a one-line wiki-relevance verdict.

If ANTHROPIC_API_KEY is unset (or the call fails), prints a graceful fallback
so the orchestrator can continue without aborting the run.

Usage:
    cat content.txt | python inbox/lib/summarize.py
"""
from __future__ import annotations

import os
import sys

MODEL = "claude-haiku-4-5-20251001"
MAX_INPUT_CHARS = 12000  # keep Haiku input bounded; items beyond this are truncated

SYSTEM_PROMPT = """\
You are summarizing items from an AI/ML news source for a reader who maintains a \
personal wiki about open-weight AI models and local inference.

The wiki covers: new open-weight model releases, local inference tools (Ollama, \
llama.cpp, LM Studio, etc.), research papers about training/inference, and \
practical AI engineering tips.

It deliberately skips: proprietary / API-only model news, hype without substance, \
and purely financial / business news.

For the item given, respond in exactly this format:

<2-3 sentence factual summary of the item>

Wiki-relevant: <reason> | Skip: <reason>

Pick "Wiki-relevant:" if the item is a new open-weight model release, a local \
inference tool, a relevant research paper, or a practical engineering tip the wiki \
would cover. Otherwise pick "Skip:" with a short reason. Output only one of the two; \
keep that verdict line to a single line.
"""

FALLBACK = "(no Haiku summary — set ANTHROPIC_API_KEY)"


def summarize(content: str) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return FALLBACK

    content = content.strip()
    if not content:
        return "(empty content — nothing to summarize)"
    if len(content) > MAX_INPUT_CHARS:
        content = content[:MAX_INPUT_CHARS] + "\n…(truncated)"

    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": content}],
        )
        parts = [block.text for block in response.content if block.type == "text"]
        text = "\n".join(parts).strip()
        return text or FALLBACK
    except Exception as exc:  # noqa: BLE001 - degrade gracefully, never abort the digest
        return f"(Haiku summary failed: {exc})"


def main() -> int:
    content = sys.stdin.read()
    print(summarize(content))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
