# Dive into Claude Code: The Design Space of AI Agent Systems

> Source: [arxiv.org/abs/2604.14228](https://arxiv.org/abs/2604.14228) · [github.com/VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) · April 14, 2026  
> Authors: Jiacheng Liu, Xiaohan Zhao, Xinyi Shang, Zhiqiang Shen (VILA Lab)

## TL;DR

A systematic reverse-engineering of Claude Code v2.1.88 (~1,900 TypeScript files, ~512K lines). The central finding: **only 1.6% of the codebase interacts with the AI model** — the rest is deterministic infrastructure. The agent loop is a trivial while-loop; the real engineering complexity is in the systems around it. The paper extracts six design principles applicable to any production AI agent.

---

## The 1.6% insight

The agent loop itself is a simple while-loop:

```
call model → run tools → repeat
```

Everything else — 98.4% of the code — is the harness around this loop:

| Component | What it does |
|-----------|-------------|
| Permission system | 7 modes + ML-based classifier; deny-first |
| Context compaction | 5-layer pipeline; graduated lazy-degradation |
| Extensibility | 4 mechanisms: MCP, plugins, skills, hooks |
| Subagent delegation | Worktree isolation; summary-only returns |
| Session storage | Append-oriented, inspectable Markdown; no permission restore on resume |

As models converge in capability, competitive advantage shifts to the harness surrounding the reasoning loop — not to the model itself.

---

## Architecture deep-dive

### Permission system

Deny-first model with seven independent safety layers plus an ML-based classifier for edge cases. Defense-in-depth — but with a shared failure mode: **all seven layers depend on preventing event-loop starvation**. Commands exceeding 50 subcommands bypass security analysis entirely.

### Context compaction pipeline

Five stages of graduated degradation, from cheapest to most destructive:
1. Prune ephemeral context (tool outputs, scratch pads)
2. Compress recent messages
3. Summarise older messages
4. Compact the full history
5. Reset (last resort)

The pipeline is lazy: it degrades only as far as needed to fit the context window. This is cost-aware design — early stages require no API calls.

### Extensibility stratified by cost

Four extension mechanisms ordered by their context cost:

| Mechanism | Cost | Use case |
|-----------|------|----------|
| Hooks | Lowest (shell, no model) | Automation triggers, logging |
| Skills | Low (inject instructions) | Reusable prompt patterns |
| Plugins | Medium | Bundled tool + context |
| MCP servers | Highest (network + model) | External service integrations |

The stratification is intentional: simple automation should not require an API call.

### Subagent delegation

Subagents run in isolated git worktrees. They return **summaries only** to the parent — not their full context. This prevents the subagent's working context (tool calls, intermediate results) from exploding the parent's context window.

### Session storage

Append-only Markdown files. Human-readable and inspectable. Permissions are **never restored on session resume** — a deliberate security choice that prioritises auditability over convenience.

---

## Five values driving the architecture

The paper traces the entire design back to five human values:

1. **Human decision authority** — the human stays in the loop; the agent proposes, the human approves
2. **Safety and security** — deny-first, layered defences
3. **Reliable execution** — cost-aware recovery, graduated degradation
4. **Capability amplification** — the harness multiplies model capability; the model doesn't have to do everything
5. **Contextual adaptability** — the system degrades gracefully rather than failing hard

---

## Six lessons for agent builders

1. **Invest in harness infrastructure** — model reasoning quality is table stakes; the harness is the differentiator
2. **Layer safety mechanisms, but map shared constraints** — seven layers sounds robust until you realise they all share one failure mode
3. **Design for context scarcity from day one** — graduated degradation is much easier to retrofit than a hard cutoff
4. **Stratify extensibility by context cost** — hooks < skills < plugins < MCP servers; match the mechanism to the use case
5. **Subagents must return summaries, not transcripts** — context explosion is the main failure mode of multi-agent systems
6. **Never restore permissions on resume** — auditability and least-privilege beat convenience at scale
