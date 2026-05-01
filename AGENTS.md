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

## Markdown conventions

- Use MkDocs Material admonitions (`!!! note`, `!!! tip`, `!!! warning`) for callouts.
- Fenced code blocks with language tags for all commands and configs.
- Tables for comparisons (models, runtimes, hardware tiers).
- Use `## TL;DR` as the first section for quick-reference notes at the top of longer pages.

## nav maintenance

`mkdocs.yml` uses an explicit `nav:` tree. When adding a new file, add it under its parent section. Sections can be nested with sub-lists. Files not listed in `nav:` are still buildable but won't appear in the sidebar.
