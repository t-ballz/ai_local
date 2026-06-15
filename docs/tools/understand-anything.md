# Understand Anything

> Source: [github.com/Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything) · MIT · v2.7.3 (May 2026)  
> ~60k GitHub stars · TypeScript + Python

## TL;DR

A plugin/CLI tool that turns a codebase into an **interactive knowledge graph** — click any function to see its dependency chain, ask natural-language questions about the code, or run `/understand-diff` before a refactor to see what will break. Works as a native Claude Code plugin, and auto-discovers itself in Cursor and VS Code. MIT licence.

---

## How it works

**Static + semantic hybrid analysis:**

1. **Tree-sitter** parses source into concrete syntax trees — deterministic extraction of imports, function signatures, class definitions
2. **LLM pass** reads the parsed structure and original source to generate plain-English summaries, architectural layer assignments, and business-domain mappings that a parser alone can't infer

**Multi-agent pipeline** (files processed concurrently, up to 5 at a time):

| Agent | Does |
|-------|------|
| `project-scanner` | Discovers files, detects languages |
| `file-analyzer` | Extracts functions/classes/imports; generates graph nodes |
| `architecture-analyzer` | Identifies layers (API, Service, Data, UI, Utility) |
| `tour-builder` | Creates guided learning paths ordered by dependency |
| `graph-reviewer` | Validates graph completeness and integrity |
| `domain-analyzer` | Maps code to business processes (`/understand-domain`) |

Output is stored in `.understand-anything/knowledge-graph.json` — commit it to skip re-analysis on every clone.

---

## Installation

**Claude Code** (native plugin):
```
/plugin marketplace add Egonex-AI/Understand-Anything
/plugin install understand-anything
```

**macOS / Linux** (one-liner, also installs for Codex, Gemini CLI, etc.):
```bash
curl -fsSL https://raw.githubusercontent.com/Egonex-AI/Understand-Anything/main/install.sh | bash
```

**Cursor** and **VS Code + Copilot** auto-discover via `.cursor-plugin/plugin.json` / `.copilot-plugin/plugin.json` after the install.

---

## Commands

| Command | Purpose |
|---------|---------|
| `/understand` | Analyse codebase; build knowledge graph |
| `/understand-dashboard` | Open interactive web visualisation |
| `/understand-chat [question]` | Ask anything about the codebase in natural language |
| `/understand-diff` | Show impact of current uncommitted changes |
| `/understand-explain [file/fn]` | Deep-dive into a specific file or function |
| `/understand-onboard` | Generate team onboarding guide |
| `/understand-domain` | Extract business domains and flows |

**Useful flags:**
- `--auto-update` — installs a post-commit hook for incremental re-analysis (only changed files)
- `--review` — runs the `graph-reviewer` agent for full LLM validation of completeness
- `--language [code]` — output in `en`, `zh`, `ja`, `ko`, `ru`, etc.

---

## Integrations

| Tool | Support |
|------|---------|
| Claude Code | Native plugin marketplace |
| Cursor | Auto-discovery |
| VS Code + Copilot (v1.108+) | Auto-discovery |
| Codex, OpenCode, Gemini CLI, Cline, Vibe CLI | `install.sh <name>` |

---

## Practical notes

- Large monorepos: scope analysis to a subdirectory rather than the full tree
- The `.understand-anything/knowledge-graph.json` file is safe to commit; for graphs over 10 MB use git-lfs
- Incremental updates (`--auto-update`) re-analyse only changed files — fast for day-to-day use after the initial run

---

## Licence

MIT — [github.com/Lum1104/Understand-Anything](https://github.com/Lum1104/Understand-Anything)
