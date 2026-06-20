# Tools

| Section | What's in it |
|---------|-------------|
| [UI Tools](ui/index.md) | Graphical interfaces for chatting with local models |
| [CLI Tools](cli/index.md) | Terminal agents and coding assistants |
| [RAG & Vector Search](turbovec.md) | turbovec — memory-efficient local vector index with TurboQuant compression |
| [Zvec](zvec.md) | Alibaba's in-process vector DB (SQLite of vector DBs); >8K QPS, no server needed |
| [LEANN](leann.md) | Low-storage vector index (MLSys 2026); 97% storage savings via on-the-fly embedding recomputation; laptop-scale RAG |
| [Hyper-Extract](hyper-extract.md) | Typed knowledge graph extraction CLI; 8 structure types, 10+ engines (GraphRAG/LightRAG/KG-Gen), 80+ YAML templates, local vLLM support |
| [Code Intelligence](understand-anything.md) | Understand Anything — codebase knowledge graph, diff impact analysis, Claude Code plugin |
| [codebase-memory-mcp](codebase-memory-mcp.md) | AST knowledge graph MCP server (arXiv:2603.27277); 158 langs, 99% token reduction, sub-ms queries, single static binary |
| **Prompt Engineering** | |
| [Priompt](priompt.md) | Cursor's open-source JSX prompt library; priority-based context management — low-priority content drops automatically when the token budget fills |
| **Robotics** | |
| [Strands Agents + LeRobot](strands-lerobot.md) | AWS + HuggingFace sim-to-hardware framework; same agent code runs in MuJoCo and physical robots; supports ACT, Diffusion Policy, SmolVLA, π0 |
| **Knowledge Synthesis** | |
| [STORM](storm.md) | Stanford multi-perspective wiki generation; simulates expert Q&A from multiple angles before writing; +25% organization, +10% coverage vs RAG baselines |
| **Dev Workflow** | |
| [spec-kit](spec-kit.md) | GitHub's spec-first AI coding workflow; 6 commands (specify→clarify→plan→tasks→implement); MIT; works with Claude Code, Cursor, Copilot, 25+ agents |
