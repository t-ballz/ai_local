# Tasks

Each file here is one wiki-writing task. Create a file, fill in the brief, then ask Claude to process it.

## File naming

```
tasks/NNNN-slug.md
```

Zero-pad the id to 4 digits. Slug is a short kebab-case description.

## Frontmatter schema

```yaml
---
id: "0001"
title: "Human-readable title"
status: todo          # todo | done
created: YYYY-MM-DD
completed: ~          # fill in when done
output: docs/<section>/<page>.md
nav: "Section > Page Title"   # where it appears in the mkdocs.yml nav tree
---
```

## Body

Write a `## Brief` section with whatever notes, instructions, or context Claude should use to write the page. The more detail you provide, the more accurate the output.

```markdown
## Brief

Cover: install steps, pulling models, running the API server, common flags.
My setup: Ubuntu 24.04, RTX 3090.
```

## How to trigger processing

Ask Claude: **"process open tasks"** or **"work on task 0003"**.

Claude will:
1. Read the brief and generate the wiki page at `output:`
2. Register the page in `mkdocs.yml` under `nav:`
3. Set `status: done` and `completed: <today>` in this file
4. Commit all three changes: `wiki: <title> [task-<id>]`

Task files are **never deleted** — the `tasks/` directory is the permanent log of what was written and when.
