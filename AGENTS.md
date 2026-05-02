# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal knowledge base about running AI locally, published as a browsable wiki via MkDocs Material.

## Wiki setup

```bash
pip install mkdocs-material        # one-time
mkdocs serve                       # live-reload dev server at http://localhost:8000
mkdocs build                       # build static site into site/
```

## Task-based workflow

All wiki content is driven by task files in `tasks/`. See `tasks/README.md` for the full schema.

**To add a page:**
1. Create `tasks/NNNN-slug.md` with YAML frontmatter (`id`, `title`, `status: todo`, `output`, `nav`) and a `## Brief` section.
2. Ask: *"process open tasks"* or *"work on task NNNN"*.

**When processing a task:**
1. Generate the wiki page at the `output:` path.
2. Add it to the `nav:` tree in `mkdocs.yml` using the task's `nav:` field.
3. Set `status: done` and `completed: <today>` in the task file.
4. Commit all changed files together:
   ```
   wiki: <title> [task-<id>]

   Co-Authored-By: AI
   ```

One commit per task — never batch. Task files are never deleted; `tasks/` is the permanent log.

**Output path conventions:**

| Topic type | Path pattern |
|------------|-------------|
| Hardware (GPU, CPU, VRAM) | `docs/hardware/<topic>.md` |
| Model notes | `docs/models/<model-family>.md` |
| Inference runtime | `docs/inference/<runtime>.md` |
| Tools / UIs | `docs/tools/<tool>.md` |

## Accuracy and honesty

**Never invent facts.** If a CLI flag, env var, URL, or version number is uncertain, say so and ask rather than guessing. Not knowing something is not an error; hiding the uncertainty is.

**When something is an approximation**, say so explicitly in the doc. Example patterns:
- Table captions: *"Sizes are Q4_K_M estimates — actual files vary by ±10–15%."*
- Inline notes: `~19 GB (approximate)` or `~19 GB¹` with a footnote.
- Admonition: `!!! note "Approximate values"` before a table built from estimates.

**When to ask instead of guess:**
- Exact CLI flag names or syntax (flags get renamed/added between releases).
- Exact env var names for third-party tools.
- Version numbers that may have changed since training cutoff.
- Any claim that would be wrong-and-harmful rather than just imprecise.

## Markdown conventions

- Use MkDocs Material admonitions (`!!! note`, `!!! tip`, `!!! warning`) for callouts.
- Fenced code blocks with language tags for all commands and configs.
- Tables for comparisons (models, runtimes, hardware tiers).
- Use `## TL;DR` as the first section for quick-reference notes at the top of longer pages.

## nav maintenance

`mkdocs.yml` uses an explicit `nav:` tree. When adding a new file, add it under its parent section. Sections can be nested with sub-lists. Files not listed in `nav:` are still buildable but won't appear in the sidebar.
