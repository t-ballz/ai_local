# Loop Engineering for Production Agents

> Source: [@_avichawla](https://x.com/_avichawla/status/2065727218991735000) · Karpathy's [AutoResearch](https://github.com/karpathy/autoresearch) · [Loop Engineering Guide](https://lushbinary.com/blog/loop-engineering-ai-coding-agents-guide/)

## The idea

Karpathy's framing:

> "Remove yourself as the bottleneck. Maximize your leverage. Put in very few tokens, and a huge amount of stuff happens on your behalf."

Most people use agents like a faster keyboard — they type a prompt, get output, type another prompt. **Loop engineering** flips this: you design a *system* that prompts the agent on a schedule against a goal, then get out of the way. Your leverage is in the system design, not the individual prompt.

---

## The minimal loop: Karpathy's AutoResearch pattern

AutoResearch (March 2026) ran **700 experiments in 2 days** on a single GPU and found 20 genuine improvements to a training pipeline — driven by one markdown file and ~630 lines of code. The structure is deliberately minimal:

| Layer | File | Role | Can the agent edit it? |
|-------|------|------|----------------------|
| Strategy | `program.md` | Defines rules: what to try, how to run, how to measure | No — human-written |
| Trust boundary | `prepare.py` | Data pipeline, tokenisation, evaluation — the fixed ground truth | No — immutable |
| Mutable genome | `train.py` | Architecture, optimiser, hyperparameters, training loop | Yes — the only target |

The loop: **propose change → commit → run (time-boxed) → parse metric → keep if improved, else revert → repeat**.

The immutable trust boundary is the critical design decision. If the agent can edit the evaluation code, it will learn to hack the metric rather than improve the model. Lock the measuring stick; only let the agent touch what it's actually supposed to improve.

---

## The production loop: six building blocks

Scaling the pattern to production agents requires more structure:

| Component | What it does |
|-----------|-------------|
| **Automations** | Recurring triggers (cron, webhook, event) that surface work without manual intervention |
| **Worktrees** | Isolated git working directories so parallel agents don't collide on files |
| **Skills** | Documented project conventions and knowledge — prevents the agent re-deriving context every run |
| **Connectors / MCP** | Integrations with external tools; stratify by cost (cheap tools first, expensive last) |
| **Sub-agents** | Separate agents for separate roles — always split the *creator* from the *verifier* |
| **Memory** | Persistent state (markdown files, issue boards) — the model forgets everything between runs |

The creator/verifier split deserves emphasis: a single agent that writes code and also decides whether the code is correct will rationalise bad output. Two agents with separate contexts produce honest disagreement.

---

## The observability layer

A loop without receipts is just an expensive cron job. For a loop to be trusted to run autonomously it needs:

### Tracing
Capture every LLM call, tool call, and decision with full context. [Opik](https://github.com/comet-ml/opik) is an open-source option (Comet ML) handling 40M+ traces/day, with 60+ framework integrations (LangChain, CrewAI, Autogen, etc.) and CI/CD PyTest hooks.

### Diagnostic agent
A second agent that reads traces and diagnoses failures — rather than you reading logs manually. The loop detects its own regressions and surfaces them as structured reports.

### Test suite
Automated evaluation harness that runs on every iteration. Define what "better" means in code before the loop starts — not after something breaks. LLM-as-judge metrics work well for subjective quality; deterministic assertions for structural correctness.

### Sandbox
All agent-generated code runs in an isolated environment (Docker, E2B, Modal) before touching anything real. The sandbox is the circuit breaker: bad outputs fail safely rather than propagating.

```
Human sets goal + rules
        ↓
Automation triggers agent
        ↓
Agent proposes change (in worktree)
        ↓
Sandbox runs it → test suite evaluates
        ↓
Tracing captures everything
        ↓
Diagnostic agent reviews traces
        ↓
Keep if improved, revert if not → repeat
```

---

## What you're actually building

The leverage isn't in the model — it's in:

1. **The stop condition** — what does "done" mean? A loop without a clear stopping criterion runs forever.
2. **The metric** — what are you actually optimising? Make it measurable before writing the first line of agent code.
3. **The trust boundary** — what can the agent not touch? Lock evaluation, config, and secrets.
4. **The memory schema** — what does the agent need to remember across runs? Design this upfront.

A well-designed loop compound-improves over time. A poorly designed one drifts, hallucinates progress, and burns budget with nothing to show.
