# spec-kit

> Source: [github/spec-kit](https://github.com/github/spec-kit) · MIT license

## TL;DR

Spec Kit implements Specification-Driven Development (SDD) — a workflow that writes detailed specifications before code, then uses AI agents to implement from the spec. Six structured commands guide you from project principles through functional specs, technical plans, and task breakdowns into implementation. Works with 30+ coding agents including Claude Code, Cursor, GitHub Copilot, and Gemini.

---

## The problem

Traditional AI coding agents excel at single-prompt code generation but struggle with:
- **Vague requirements** that lead to building the wrong thing
- **Lack of shared context** across a long development process
- **No validation** that the implementation matches the specification
- **Rework loops** because the spec wasn't clear before coding started

Spec Kit inverts this: write the spec first, make it executable, then generate implementation from it.

---

## How it works

The workflow follows seven phases, spanning six core commands:

| Command | Phase | What it does |
|---------|-------|-------------|
| `/speckit.constitution` | 1 | Establish project governance principles and development guidelines that inform all technical decisions |
| `/speckit.specify` | 2 | Define functional requirements and user stories (focus on *what* and *why*, not the tech stack) |
| `/speckit.clarify` | 3 | Use structured questioning to resolve vague or underspecified requirements *before* planning |
| `/speckit.plan` | 4 | Create a technical implementation strategy: tech stack, architecture, major components |
| `/speckit.tasks` | 5 | Break the plan into ordered, actionable tasks with dependency relationships and test structure |
| `/speckit.implement` | 6 | Execute all tasks systematically; the AI agent builds the implementation, respecting task order and dependencies |
| (validation) | 7 | Assess codebase against spec/plan/tasks; append remaining work as new tasks if needed |

**Key insight**: Each command produces structured, stored artifacts (in `.specify/memory/`) that the next command builds on. The AI agent doesn't start from scratch each time — it reads the full context of what was decided before.

---

## Setup / usage

### Install

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@vX.Y.Z
```

Replace `vX.Y.Z` with the latest release tag. Alternative: use `pipx` instead of `uv`.

**Requirements**: Python 3.11+, Git, and a supported AI coding agent (Claude Code, Cursor, GitHub Copilot, Gemini, etc.).

### Create a project

```bash
specify init my-project --integration copilot
cd my-project
```

Specify your agent during init, or let the CLI auto-detect.

### Run the workflow

1. Start your coding agent (Copilot, Claude Code, etc.) in the project directory
2. Use the slash commands in order: constitution → specify → clarify → plan → tasks → implement
3. Each command reads the outputs from previous steps, so context flows through the entire development lifecycle

### Example

**Specification** (from `/speckit.specify`):
> "Build an application that organizes photos into albums grouped by date, with drag-and-drop reorganization and tile-like photo previews."

**Plan** (from `/speckit.plan`):
> "Tech stack: Vite + vanilla JavaScript + HTML/CSS. Images stored locally; metadata in SQLite. No cloud upload."

**Tasks** (from `/speckit.tasks`):
> 1. Set up Vite project structure
> 2. Create SQLite schema for photo metadata
> 3. Build photo tile component
> 4. Implement drag-and-drop reordering
> 5. Add date-based grouping logic
> ... (continues in dependency order)

**Implement** (from `/speckit.implement`):
> The agent executes each task in order, following the tech stack and architecture from the plan.

---

## Why it matters

**Specification-first prevents costly mistakes**: Ambiguous specs lead to building the wrong feature, requiring rework. Spec Kit forces clarity upfront through structured questioning and executive-level planning *before* code is written.

**Scales across teams**: The `.specify/memory/` directory stores all decisions (constitution, specs, plans, task lists). Team members can read the full context, and multiple agents can work in parallel on different tasks without losing alignment.

**Reduces agent hallucination**: Instead of asking an AI agent "build me a photo app," you give it a detailed spec ("here's the tech stack, here's the schema, here's task 3 of 15: implement drag-and-drop"). The agent's scope is tightly bounded, and it can validate its work against the spec.

**Extensions and presets**: The system is extensible — add Jira integration, code review workflows, or custom templates without modifying core commands. Presets let teams enforce organizational standards (linting rules, deployment targets, code review gates).

---

## Source

- **GitHub**: [github/spec-kit](https://github.com/github/spec-kit)
- **License**: MIT
- **Supported agents**: 30+ integrations including Claude Code, Cursor, GitHub Copilot, Gemini, and others
- **Documentation**: [github.github.io/spec-kit/](https://github.github.io/spec-kit/)
