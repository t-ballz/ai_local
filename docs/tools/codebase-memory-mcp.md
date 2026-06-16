# codebase-memory-mcp

> Source: [arXiv:2603.27277](https://arxiv.org/abs/2603.27277) · March 2026  
> GitHub: [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)

## TL;DR

An MCP server that indexes codebases as persistent AST knowledge graphs using Tree-Sitter, then exposes 14 typed graph-query tools to any connected agent. Instead of agents reading files one by one, they query a pre-built structural graph — functions, classes, HTTP routes, cross-service call chains — in sub-millisecond time. Single static binary, no Docker, no API keys, no runtime dependencies. Indexes the Linux kernel (28M LOC, 75K files) in 3 minutes.

---

## The problem

LLM coding agents explore codebases through repeated file reads and grep calls. Each structural question ("what calls this function?", "where is this type defined?") consumes thousands of tokens and multiple tool calls without building any persistent structural understanding. The knowledge is thrown away after each query.

---

## How it works

### Indexing pipeline

1. **Tree-Sitter parsing** — 158 languages parsed into ASTs via vendored grammars
2. **Parallel extraction** — worker pools extract symbols (functions, classes, interfaces, routes) concurrently
3. **Call-graph construction** — 6-strategy call resolution; hybrid LSP semantic resolution for 10 major languages (Python, TypeScript/JS/JSX/TSX, Go, Rust, Java, C/C++, Kotlin, C#, PHP) refines edges using the import graph and a cross-file definition registry
4. **Community detection** — Louvain algorithm clusters related code into architectural modules
5. **Impact analysis** — precomputed reverse edges for change-impact queries
6. **Persistence** — SQLite (WAL mode) at `~/.cache/codebase-memory-mcp/`; optional zstd-compressed snapshots (8–13:1 ratio) for team sharing via `.codebase-memory/graph.db.zst`

### Querying

Agents issue Cypher-like traversal queries through the 14 MCP tools. Structural queries are resolved in sub-millisecond time against the graph rather than re-reading source files.

---

## Benchmarks

Evaluated on 31 real-world repositories (paper: arXiv:2603.27277):

| Metric | File-exploration baseline | codebase-memory-mcp |
|--------|--------------------------|---------------------|
| Tokens (structural queries) | baseline | **99% fewer** |
| Tokens (overall) | baseline | ~10× fewer |
| Answer quality | 92% | 83% |
| Tool calls | baseline | **2.1× fewer** |
| Graph-native tasks | — | Matched or exceeded on 19/31 repos |

The accuracy gap (83% vs 92%) reflects a tradeoff: the graph represents structure, not full semantics. For architectural questions it excels; for questions requiring reading raw logic, file access is still needed.

---

## 14 MCP tools

| Category | Tools |
|----------|-------|
| **Indexing** | `index_repository`, `list_projects`, `delete_project`, `index_status` |
| **Graph queries** | `search_graph`, `query_graph`, `get_graph_schema`, `trace_path` |
| **Code access** | `get_code_snippet`, `search_code` |
| **Analysis** | `get_architecture`, `detect_changes`, `manage_adr`, `ingest_traces` |

`trace_path` — call-path tracing between any two symbols  
`detect_changes` — diff-aware impact analysis (which callers are affected by a change)  
`get_architecture` — Louvain community view of the codebase's module structure

---

## Installation

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/install.sh | bash
```

The installer auto-detects 11 agents (Claude Code, Codex CLI, Gemini CLI, Zed, VS Code, and others) and configures them automatically — MCP server entries, custom instructions, and for Claude Code, pre-tool hooks that augment grep/glob calls with graph context.

**Manual Claude Code config** (`~/.claude/.mcp.json`):

```json
{
  "mcpServers": {
    "codebase-memory-mcp": {
      "command": "/path/to/codebase-memory-mcp"
    }
  }
}
```

Build from source requires a C/C++ compiler + zlib; `scripts/build.sh` handles it.

---

## Language support

158 languages via vendored tree-sitter grammars. Quality tiers:

| Tier | Languages |
|------|-----------|
| Excellent (≥90%) | C, C++, Kotlin, Swift, Lua, Bash, HTML |
| Good (75–89%) | Python, TypeScript, Go, Rust, Java, PHP, C# |

LSP-enhanced semantic resolution (import-graph + cross-file definition registry) available for: Python, TypeScript/JS/JSX/TSX, Go, Rust, Java, C, C++, Kotlin, PHP, C#.

---

## Limitations

- Answer quality drops to 83% (vs 92% for file-by-file) on tasks requiring full code semantics — the graph captures structure, not logic
- Cypher write operations, `MERGE`, and list/map literals are unsupported
- Windows SmartScreen may flag the binary (verify via checksums; SLSA Level 3 provenance + cosign signatures provided)
- Per-project language extension requires `.codebase-memory.json` config

---

## Source

- **Paper**: [arXiv:2603.27277](https://arxiv.org/abs/2603.27277)
- **GitHub**: [DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)
- **Docs**: [deusdata.github.io/codebase-memory-mcp](https://deusdata.github.io/codebase-memory-mcp/)
