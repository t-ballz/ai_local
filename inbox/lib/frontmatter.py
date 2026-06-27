"""Stdlib-only YAML-subset frontmatter parser/serializer.

Supported value types: str, int, bool, None, list[str].
No nested maps, no multiline scalars.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def _needs_quoting(s: str) -> bool:
    if not s or s != s.strip():
        return True
    if any(c in s for c in ':#"\'[]{},'):
        return True
    if s in ("true", "false", "null"):
        return True
    try:
        int(s)
        return True
    except ValueError:
        pass
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False


def _scalar_to_yaml(v: object) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, list):
        parts = []
        for item in v:
            s = str(item)
            parts.append(f'"{s}"' if _needs_quoting(s) else s)
        return "[" + ", ".join(parts) + "]"
    s = str(v)
    if _needs_quoting(s):
        escaped = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return s


def _yaml_to_scalar(s: str) -> object:
    s = s.strip()
    if s == "null":
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        items = []
        for item in inner.split(","):
            item = item.strip()
            if item.startswith('"') and item.endswith('"'):
                item = item[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            elif item.startswith("'") and item.endswith("'"):
                item = item[1:-1]
            items.append(item)
        return items
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if s.startswith("'") and s.endswith("'"):
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    return s


def parse(text: str) -> tuple[dict, str]:
    """Split a frontmatter document into (metadata, body).

    Returns ({}, text) if no leading '---' fence.
    Raises ValueError on malformed/unterminated fence.
    """
    if not text.startswith("---\n"):
        return {}, text
    rest = text[4:]
    lines = rest.split("\n")
    close_idx = None
    for i, line in enumerate(lines):
        if line.rstrip() == "---":
            close_idx = i
            break
    if close_idx is None:
        raise ValueError("Unterminated frontmatter fence")
    fm_lines = lines[:close_idx]
    body = "\n".join(lines[close_idx + 1:]).lstrip("\n").rstrip()
    meta: dict = {}
    for line in fm_lines:
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val_raw = line.partition(":")
        meta[key.strip()] = _yaml_to_scalar(val_raw.strip())
    return meta, body


def dump(meta: dict, body: str) -> str:
    """Serialize (metadata, body) to a frontmatter document."""
    lines = ["---"]
    for key, value in meta.items():
        lines.append(f"{key}: {_scalar_to_yaml(value)}")
    lines.append("---")
    lines.append("")
    if body:
        lines.append(body.rstrip())
    return "\n".join(lines) + "\n"


def read(path: "str | Path") -> tuple[dict, str]:
    return parse(Path(path).read_text(encoding="utf-8"))


def write(path: "str | Path", meta: dict, body: str) -> None:
    content = dump(meta, body)
    p = Path(path)
    fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=".fm_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, p)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    sample_meta = {
        "id": "2606.16222",
        "title": "Latent Thought Flow: Efficient Reasoning, Test",
        "url": "https://arxiv.org/abs/2606.16222",
        "score": 4,
        "tags": ["rl", "reasoning"],
        "status": "filed",
        "wiki_page": None,
    }
    sample_body = "## Summary\nThis is the body.\n\n## Verdict\nWiki-relevant."
    doc = dump(sample_meta, sample_body)
    print(doc)
    meta2, body2 = parse(doc)
    assert meta2 == sample_meta, f"meta mismatch: {meta2}"
    assert body2 == sample_body.rstrip(), f"body mismatch: {body2!r}"
    print("Round-trip OK")
