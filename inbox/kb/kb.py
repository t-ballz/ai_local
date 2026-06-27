#!/usr/bin/env python3
"""Knowledge base CLI for the inbox pipeline.

Usage: python inbox/kb/kb.py <subcommand> [flags]

Subcommands:
  file          File an item from stdin JSON into inbox/kb/items/
  reindex       Rebuild index.db from all item files
  query         Search the index
  related       Find related items by tag overlap
  promote-stub  Generate a wiki page stub and mark the item promoted
  validate      Check all item files against the schema
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import frontmatter  # noqa: E402

# ---------------------------------------------------------------------------
# Paths & constants
# ---------------------------------------------------------------------------

KB_DIR = Path(__file__).resolve().parent
ITEMS_DIR = KB_DIR / "items"
TAGS_FILE = KB_DIR / "tags.md"
DB_PATH = KB_DIR / "index.db"
REPO_ROOT = KB_DIR.parents[1]

VALID_RELEVANCE = {"wiki-relevant", "minor", "skip"}
VALID_STATUS = {"filed", "promoted", "dropped"}
PAPER_SOURCES = {"huggingface-papers"}

FIELD_ORDER = [
    "id", "title", "url", "source", "filed", "digest",
    "relevance", "score", "tags", "status", "wiki_page", "arxiv",
]


# ---------------------------------------------------------------------------
# ID sanitization
# ---------------------------------------------------------------------------

def sanitize_id(id_: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", id_)
    safe = re.sub(r"_+", "_", safe).strip("_")
    return safe or "item"


def _disambiguate(stem: str, id_: str) -> str:
    suffix = hashlib.sha1(id_.encode()).hexdigest()[:6]
    return f"{stem}-{suffix}"


def item_path(id_: str, filed: datetime.date) -> Path:
    """Compute the canonical path for a new item file (never rewrites existing paths)."""
    stem = sanitize_id(id_)
    year = f"{filed.year:04d}"
    month = f"{filed.month:02d}"
    candidate = ITEMS_DIR / year / month / f"{stem}.md"
    if candidate.exists():
        try:
            existing_meta, _ = frontmatter.read(candidate)
            if existing_meta.get("id") != id_:
                stem = _disambiguate(stem, id_)
                candidate = ITEMS_DIR / year / month / f"{stem}.md"
        except (ValueError, OSError):
            pass
    return candidate


def find_item_path(id_: str) -> Path | None:
    """Find the path of an existing item by id, using the DB if available."""
    if DB_PATH.exists():
        try:
            conn = _connect()
            row = conn.execute("SELECT path FROM items WHERE id = ?", (id_,)).fetchone()
            conn.close()
            if row:
                p = REPO_ROOT / row["path"]
                return p if p.exists() else None
        except Exception:  # noqa: BLE001
            pass
    # Fallback: scan items dir
    for f in ITEMS_DIR.rglob("*.md"):
        try:
            meta, _ = frontmatter.read(f)
            if meta.get("id") == id_:
                return f
        except (ValueError, OSError):
            pass
    return None


# ---------------------------------------------------------------------------
# Tag vocabulary
# ---------------------------------------------------------------------------

def load_tags() -> set[str]:
    if not TAGS_FILE.exists():
        return set()
    tags: set[str] = set()
    for line in TAGS_FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"-\s+`([a-z0-9-]+)`", line.strip())
        if m:
            tags.add(m.group(1))
    return tags


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id        TEXT PRIMARY KEY,
            path      TEXT NOT NULL,
            title     TEXT,
            url       TEXT,
            source    TEXT,
            filed     TEXT,
            digest    TEXT,
            relevance TEXT,
            score     INTEGER,
            tags      TEXT,
            status    TEXT,
            wiki_page TEXT,
            arxiv     TEXT
        )
    """)
    conn.commit()


def _tags_str(tags: list[str] | None) -> str:
    return " " + " ".join(tags or []) + " "


def _upsert(conn: sqlite3.Connection, meta: dict, path: Path) -> None:
    rel = str(path.relative_to(REPO_ROOT)) if path.is_absolute() else str(path)
    conn.execute("""
        INSERT OR REPLACE INTO items
          (id, path, title, url, source, filed, digest, relevance, score,
           tags, status, wiki_page, arxiv)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        meta.get("id"),
        rel,
        meta.get("title"),
        meta.get("url"),
        meta.get("source"),
        meta.get("filed"),
        meta.get("digest"),
        meta.get("relevance"),
        meta.get("score"),
        _tags_str(meta.get("tags")),
        meta.get("status"),
        meta.get("wiki_page"),
        meta.get("arxiv"),
    ))
    conn.commit()


def _rebuild(conn: sqlite3.Connection) -> int:
    conn.execute("DROP TABLE IF EXISTS items")
    _schema(conn)
    count = 0
    for item_file in sorted(ITEMS_DIR.rglob("*.md")):
        try:
            meta, _ = frontmatter.read(item_file)
            if "id" not in meta:
                continue
            _upsert(conn, meta, item_file)
            count += 1
        except Exception:  # noqa: BLE001
            continue
    return count


# ---------------------------------------------------------------------------
# Item building
# ---------------------------------------------------------------------------

def build_meta(record: dict, filed: datetime.date, status: str) -> dict:
    id_ = str(record.get("id") or "").strip()
    if not id_:
        raise ValueError("record missing 'id'")
    title = str(record.get("title") or "").strip()
    if not title:
        raise ValueError("record missing 'title'")
    relevance = str(record.get("relevance") or "").strip().lower()
    if relevance not in VALID_RELEVANCE:
        raise ValueError(f"invalid relevance {relevance!r}; must be one of {sorted(VALID_RELEVANCE)}")
    if status not in VALID_STATUS:
        raise ValueError(f"invalid status {status!r}")
    try:
        score = int(record.get("score"))
    except (TypeError, ValueError):
        raise ValueError(f"invalid score {record.get('score')!r}; must be integer 0-5")
    if not 0 <= score <= 5:
        raise ValueError(f"score {score} out of range 0-5")
    tags = list(record.get("tags") or [])
    source = str(record.get("source") or "")
    arxiv = id_ if source in PAPER_SOURCES else record.get("arxiv")
    today = filed.isoformat()
    return {
        "id": id_,
        "title": title,
        "url": str(record.get("url") or ""),
        "source": source,
        "filed": today,
        "digest": str(record.get("digest") or today),
        "relevance": relevance,
        "score": score,
        "tags": tags,
        "status": status,
        "wiki_page": record.get("wiki_page"),
        "arxiv": arxiv,
    }


def render_body(record: dict) -> str:
    summary = str(record.get("summary") or "").strip()
    verdict = str(record.get("verdict") or "").strip()
    parts = []
    if summary:
        parts.append(f"## Summary\n{summary}")
    if verdict:
        parts.append(f"## Verdict\n{verdict}")
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Subcommand: file
# ---------------------------------------------------------------------------

def cmd_file(args: argparse.Namespace) -> int:
    try:
        record = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON on stdin: {e}", file=sys.stderr)
        return 1

    filed_str = args.filed or datetime.date.today().isoformat()
    try:
        filed = datetime.date.fromisoformat(filed_str)
    except ValueError:
        print(f"error: invalid --filed date {filed_str!r}", file=sys.stderr)
        return 1

    try:
        meta = build_meta(record, filed, args.status)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    known = load_tags()
    for tag in meta["tags"]:
        if tag.startswith("?"):
            print(f"warning: proposed new tag {tag!r}", file=sys.stderr)
        elif known and tag not in known:
            print(f"warning: unknown tag {tag!r} (not in tags.md)", file=sys.stderr)

    path = item_path(meta["id"], filed)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists() and not args.force:
        try:
            _, existing_body = frontmatter.read(path)
        except ValueError as e:
            print(f"error: existing file malformed ({e}); use --force to overwrite", file=sys.stderr)
            return 2
        body = existing_body
    else:
        body = render_body(record)

    try:
        frontmatter.write(path, meta, body)
    except OSError as e:
        print(f"error writing {path}: {e}", file=sys.stderr)
        return 2

    # Best-effort DB upsert — never abort on DB errors
    try:
        conn = _connect()
        _schema(conn)
        _upsert(conn, meta, path)
        conn.close()
    except Exception:  # noqa: BLE001
        pass

    print(str(path.relative_to(REPO_ROOT)))
    return 0


# ---------------------------------------------------------------------------
# Subcommand: reindex
# ---------------------------------------------------------------------------

def cmd_reindex(args: argparse.Namespace) -> int:
    try:
        conn = _connect()
        count = _rebuild(conn)
        conn.close()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(f"{count} items indexed")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: query
# ---------------------------------------------------------------------------

def cmd_query(args: argparse.Namespace) -> int:
    if not DB_PATH.exists():
        print("error: index.db not found — run: python inbox/kb/kb.py reindex", file=sys.stderr)
        return 2
    try:
        conn = _connect()
        _schema(conn)
        clauses: list[str] = []
        params: list[object] = []
        for tag in (args.tag or []):
            clauses.append("tags LIKE ?")
            params.append(f"% {tag} %")
        if args.source:
            clauses.append("source = ?")
            params.append(args.source)
        if args.relevance:
            clauses.append("relevance = ?")
            params.append(args.relevance)
        if args.min_score is not None:
            clauses.append("score >= ?")
            params.append(args.min_score)
        if args.status:
            clauses.append("status = ?")
            params.append(args.status)
        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        rows = conn.execute(
            f"SELECT * FROM items {where} ORDER BY score DESC, filed DESC, id",
            params,
        ).fetchall()
        conn.close()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([dict(r) for r in rows], indent=2))
    else:
        for r in rows:
            tags = (r["tags"] or "").strip()
            print(f"{r['score']:2d}  {r['id']:<32}  {(r['title'] or '')[:60]}  [{tags}]")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: related
# ---------------------------------------------------------------------------

def cmd_related(args: argparse.Namespace) -> int:
    if not DB_PATH.exists():
        print("error: index.db not found — run: python inbox/kb/kb.py reindex", file=sys.stderr)
        return 2
    try:
        conn = _connect()
        _schema(conn)
        row = conn.execute("SELECT tags FROM items WHERE id = ?", (args.id,)).fetchone()
        if not row:
            print(f"error: id {args.id!r} not found in index", file=sys.stderr)
            conn.close()
            return 1
        target_tags = set((row["tags"] or "").split())
        all_rows = conn.execute(
            "SELECT id, title, score, tags FROM items WHERE id != ?", (args.id,)
        ).fetchall()
        conn.close()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not target_tags:
        print("(no tags on this item — no related items found)")
        return 0

    scored: list[tuple[int, int, str, str]] = []
    for r in all_rows:
        other_tags = set((r["tags"] or "").split())
        shared = len(target_tags & other_tags)
        if shared > 0:
            scored.append((shared, int(r["score"] or 0), str(r["id"]), str(r["title"] or "")))
    scored.sort(key=lambda x: (-x[0], -x[1]))

    if args.json:
        out = [{"shared": s, "score": sc, "id": i, "title": t} for s, sc, i, t in scored[:args.limit]]
        print(json.dumps(out, indent=2))
    else:
        for shared, score, id_, title in scored[:args.limit]:
            print(f"{shared:2d} shared  score={score}  {id_:<32}  {title[:60]}")
    return 0


# ---------------------------------------------------------------------------
# Subcommand: promote-stub
# ---------------------------------------------------------------------------

def _slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug[:80]


def cmd_promote_stub(args: argparse.Namespace) -> int:
    if not DB_PATH.exists():
        print("error: index.db not found — run reindex first", file=sys.stderr)
        return 2
    try:
        conn = _connect()
        row = conn.execute("SELECT * FROM items WHERE id = ?", (args.id,)).fetchone()
        conn.close()
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    if not row:
        print(f"error: id {args.id!r} not found", file=sys.stderr)
        return 1

    section = args.section
    slug = _slugify(str(row["title"] or args.id))
    wiki_rel = f"docs/{section}/{slug}.md"
    wiki_path = REPO_ROOT / wiki_rel

    if wiki_path.exists() and not args.dry_run:
        print(f"error: {wiki_rel} already exists", file=sys.stderr)
        return 1

    arxiv = row["arxiv"]
    url = row["url"] or ""
    if arxiv:
        source_line = f"> Source: [arXiv:{arxiv}](https://arxiv.org/abs/{arxiv})"
    elif url:
        domain = urlparse(url).netloc or url
        source_line = f"> Source: [{domain}]({url})"
    else:
        source_line = "> Source: (unknown)"

    stub = f"""# {row['title']}

{source_line}

## TL;DR

<!-- One paragraph summary -->

## How It Works

<!-- Key technical details -->

## Results

<!-- Benchmarks, numbers, comparisons -->

## Notes

<!-- Personal observations, limitations, open questions -->
"""

    if args.dry_run:
        print(stub)
        print(f"# Would write to: {wiki_rel}", file=sys.stderr)
        return 0

    wiki_path.parent.mkdir(parents=True, exist_ok=True)
    wiki_path.write_text(stub, encoding="utf-8")

    # Update the item's status and wiki_page
    item_file = REPO_ROOT / row["path"]
    try:
        item_meta, item_body = frontmatter.read(item_file)
        item_meta["status"] = "promoted"
        item_meta["wiki_page"] = wiki_rel
        frontmatter.write(item_file, item_meta, item_body)
        conn = _connect()
        item_meta_copy = dict(row)
        item_meta_copy["status"] = "promoted"
        item_meta_copy["wiki_page"] = wiki_rel
        _upsert(conn, item_meta_copy, item_file)
        conn.close()
    except Exception as e:  # noqa: BLE001
        print(f"warning: could not update item status: {e}", file=sys.stderr)

    print(wiki_rel)
    return 0


# ---------------------------------------------------------------------------
# Subcommand: validate
# ---------------------------------------------------------------------------

def cmd_validate(args: argparse.Namespace) -> int:
    known_tags = load_tags()
    errors: list[str] = []
    warnings: list[str] = []
    count = 0
    for item_file in sorted(ITEMS_DIR.rglob("*.md")):
        count += 1
        try:
            meta, body = frontmatter.read(item_file)
        except (ValueError, OSError) as e:
            errors.append(f"{item_file.relative_to(REPO_ROOT)}: parse error: {e}")
            continue
        rel = str(item_file.relative_to(REPO_ROOT))
        for key in FIELD_ORDER:
            if key not in meta:
                errors.append(f"{rel}: missing key '{key}'")
        if meta.get("relevance") not in VALID_RELEVANCE:
            errors.append(f"{rel}: invalid relevance {meta.get('relevance')!r}")
        if meta.get("status") not in VALID_STATUS:
            errors.append(f"{rel}: invalid status {meta.get('status')!r}")
        score = meta.get("score")
        if not isinstance(score, int) or not 0 <= score <= 5:
            errors.append(f"{rel}: invalid score {score!r}")
        for tag in (meta.get("tags") or []):
            if tag.startswith("?"):
                warnings.append(f"{rel}: proposed tag {tag!r}")
            elif known_tags and tag not in known_tags:
                warnings.append(f"{rel}: unknown tag {tag!r}")
        if not body.strip():
            warnings.append(f"{rel}: empty body")

    if args.json:
        print(json.dumps({"count": count, "errors": errors, "warnings": warnings}, indent=2))
    else:
        print(f"Validated {count} items: {len(errors)} errors, {len(warnings)} warnings")
        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN:  {w}")
    return 1 if errors else 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="kb.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_file = sub.add_parser("file")
    p_file.add_argument("--filed", help="Filed date YYYY-MM-DD (default: today)")
    p_file.add_argument("--status", default="filed", choices=["filed", "promoted", "dropped"])
    p_file.add_argument("--force", action="store_true")

    sub.add_parser("reindex")

    p_query = sub.add_parser("query")
    p_query.add_argument("--tag", action="append")
    p_query.add_argument("--source")
    p_query.add_argument("--relevance", choices=["wiki-relevant", "minor", "skip"])
    p_query.add_argument("--min-score", type=int, dest="min_score")
    p_query.add_argument("--status", choices=["filed", "promoted", "dropped"])
    p_query.add_argument("--json", action="store_true")

    p_related = sub.add_parser("related")
    p_related.add_argument("id")
    p_related.add_argument("--limit", type=int, default=10)
    p_related.add_argument("--json", action="store_true")

    p_stub = sub.add_parser("promote-stub")
    p_stub.add_argument("id")
    p_stub.add_argument("--section", default="research",
                        choices=["research", "models", "tools", "software-thoughts"])
    p_stub.add_argument("--dry-run", action="store_true", dest="dry_run")

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    handlers = {
        "file": cmd_file,
        "reindex": cmd_reindex,
        "query": cmd_query,
        "related": cmd_related,
        "promote-stub": cmd_promote_stub,
        "validate": cmd_validate,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
