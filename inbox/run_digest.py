#!/usr/bin/env python3
"""Daily digest orchestrator for the inbox.

For each source under inbox/sources/*/:
  1. Run enumerate.py to discover new items (JSON array on stdout).
  2. For each item, run the source's fetch.py {id}, pipe content to
     lib/summarize.py, and collect the Haiku summary + wiki-relevance verdict.
  3. Format a markdown digest grouped by source.
  4. Write it to inbox/digests/YYYY-MM-DD.md and print it to stdout.

Per-item and per-source failures are caught and noted inline; one broken source
never aborts the whole run.

Usage:
    python inbox/run_digest.py [--dry-run]

--dry-run is forwarded to each enumerate.py so last_seen pointers are not advanced.
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

INBOX_DIR = Path(__file__).resolve().parent
SOURCES_DIR = INBOX_DIR / "sources"
DIGESTS_DIR = INBOX_DIR / "digests"
SUMMARIZE = INBOX_DIR / "lib" / "summarize.py"

# pending Twitter items added manually via the add-tweet skill
TWITTER_PENDING = SOURCES_DIR / "twitter-follows" / "pending.json"


def run(cmd: list[str], *, stdin: str | None = None, timeout: int = 120) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        input=stdin,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def enumerate_source(source_dir: Path, dry_run: bool) -> tuple[list[dict], str | None]:
    """Run a source's enumerate.py and return (items, cap_warning | None)."""
    script = source_dir / "enumerate.py"
    if not script.exists():
        raise FileNotFoundError(f"no enumerate.py in {source_dir.name}")
    cmd = [sys.executable, str(script)]
    if dry_run:
        cmd.append("--dry-run")
    proc = run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"enumerate.py exited {proc.returncode}")
    out = proc.stdout.strip()
    items = json.loads(out) if out else []
    warning: str | None = None
    for line in (proc.stderr or "").splitlines():
        if line.startswith("CAP_WARNING:"):
            warning = line[len("CAP_WARNING:"):].strip()
            break
    return items, warning


def fetch_and_summarize(source_dir: Path, item_id: str) -> str:
    """Fetch full item content and summarize it. Returns the summary text."""
    fetch = source_dir / "fetch.py"
    if not fetch.exists():
        return "(no fetch.py for this source)"
    proc = run([sys.executable, str(fetch), item_id])
    if proc.returncode != 0:
        return f"(fetch failed: {proc.stderr.strip() or proc.returncode})"
    content = proc.stdout
    sproc = run([sys.executable, str(SUMMARIZE)], stdin=content)
    if sproc.returncode != 0:
        return f"(summarize failed: {sproc.stderr.strip() or sproc.returncode})"
    return sproc.stdout.strip()


def load_twitter_pending() -> list[dict]:
    if not TWITTER_PENDING.exists():
        return []
    try:
        data = json.loads(TWITTER_PENDING.read_text())
        return data if isinstance(data, list) else []
    except Exception:  # noqa: BLE001
        return []


def format_item(index: int, item: dict, summary: str) -> str:
    title = item.get("title") or "(untitled)"
    url = item.get("url") or ""
    lines = [f"### {index}. {title}"]
    if url:
        lines.append(f"<{url}>")
    lines.append("")
    lines.append(summary or "(no summary)")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]

    today = datetime.date.today().isoformat()
    sections: list[str] = []
    item_counter = 0

    source_dirs = sorted(p for p in SOURCES_DIR.glob("*") if p.is_dir())

    for source_dir in source_dirs:
        name = source_dir.name
        section_lines = [f"## {name}", ""]

        try:
            items, cap_warning = enumerate_source(source_dir, dry_run)
        except Exception as exc:  # noqa: BLE001 - skip this source, keep going
            section_lines.append(f"_Error enumerating: {exc}_")
            section_lines.append("")
            sections.append("\n".join(section_lines))
            continue

        if cap_warning:
            section_lines.append(f"> ⚠ **Cap reached:** {cap_warning}")
            section_lines.append("")

        # Merge manually-added pending Twitter items into that source.
        if name == "twitter-follows":
            pending = load_twitter_pending()
            for p in pending:
                items.append(
                    {
                        "id": p.get("id", ""),
                        "title": p.get("title", "(tweet)"),
                        "url": p.get("url", ""),
                        "snippet": p.get("snippet", ""),
                        "_pending_summary": p.get("summary", ""),
                    }
                )

        if not items:
            section_lines.append("_No new items._")
            section_lines.append("")
            sections.append("\n".join(section_lines))
            continue

        for item in items:
            item_counter += 1
            item_id = item.get("id", "")
            # Pending Twitter items already carry a summary — don't refetch.
            if item.get("_pending_summary"):
                summary = item["_pending_summary"]
            else:
                try:
                    summary = fetch_and_summarize(source_dir, item_id)
                except Exception as exc:  # noqa: BLE001
                    summary = f"(error: {exc})"
            section_lines.append(format_item(item_counter, item, summary))

        sections.append("\n".join(section_lines))

    header = f"# Digest — {today}\n"
    if dry_run:
        header += "\n_(dry run — last_seen pointers not advanced)_\n"
    digest = header + "\n" + "\n".join(sections)
    digest = digest.rstrip() + "\n"

    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIGESTS_DIR / f"{today}.md"
    out_path.write_text(digest)

    print(digest)
    print(f"\n(written to {out_path})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
