# LedgerAgent: Structured State for Policy-Adherent Tool-Calling Agents

> Source: [arXiv:2606.20529](https://arxiv.org/abs/2606.20529) · June 18, 2026  
> Authors: Md Nayem Uddin, Amir Saeidi, Eduardo Blanco, Chitta Baral

## TL;DR

Tool-calling agents fail when they lose track of task state across turns or violate domain policies. LedgerAgent maintains an explicit ledger of verified facts, constraints, and identifiers separate from the prompt, checking policy compliance before each action. No model retraining required—pure deterministic state management at inference time.

---

## The problem with implicit state

Standard agents embed observations, tool returns, and policy instructions directly in the prompt. The model must reconstruct relevant task state fresh each turn from a growing transcript. This creates two critical failure modes:

1. **Stale state**: The agent retrieves the right facts but grounds later decisions in outdated, missing, or incorrect information accumulated across multiple turns.
2. **Policy violations**: A syntactically valid tool call may still violate domain constraints that depend on the current task state—e.g., refunding an order without checking if a refund is already pending.

In customer-service domains where consistency and policy adherence are non-negotiable, these failures compound across multi-turn interactions.

---

## LedgerAgent: explicit structured state

The core insight: separate state management from reasoning by maintaining a **ledger** parallel to the conversation.

### Components

**1. State Ledger**
- Maintains a structured record of observed task facts: entity identifiers, constraints, conditions, and outcomes
- Facts are added only after tool execution confirms them (verified state, not assumed)
- Examples: `customer_id`, `order_status`, `refund_eligibility`, `pending_actions`

**2. Ledger-to-Prompt Rendering**
- The current ledger state is rendered explicitly into the prompt before each decision
- Gives the model a clean, consistent view of what is known about the task
- Prevents the model from having to mine task state from conversational history

**3. Policy Constraint Checking**
- Before executing any environment-changing tool call, the ledger validates state-dependent policies
- Blocking happens deterministically at inference time, not via model judgment
- Example: block a refund if `refund_eligibility: False` is already recorded

### Why it works

- **No retraining**: inference-time method; works with any tool-calling LLM
- **No extra LLM calls**: validation is deterministic, not generative
- **Explicit recovery**: when a tool call is blocked, the model sees why and can adjust its strategy
- **Audit trail**: the ledger forms a complete record of all verified facts and policy decisions

---

## Key results

Evaluated across four customer-service domains (order support, billing, returns, account management) with both open-weight and closed-weight models:

- **Pass@k consistency**: LedgerAgent improves average pass@k over standard prompt-based baseline
- **Largest gains under strict metrics**: Multi-trial consistency metrics show the biggest improvements—exactly where implicit state fails most
- **Model-agnostic**: improvements hold across different LLM architectures

Compared to prompt-engineering baselines, LedgerAgent trades minimal inference overhead (ledger updates and policy checks) for reliable state coherence and policy compliance.

---

## Why it matters

1. **Reliability for regulated domains**: Customer-service agents must comply with domain policies deterministically. Implicit state makes this almost impossible to guarantee.

2. **Scales with interaction complexity**: As conversations lengthen and stakes rise, implicit state reconstruction gets exponentially harder. A ledger prevents this degradation.

3. **Practical for production**: No model fine-tuning, no additional API calls, no change to the agent's decision loop—just a thin state management layer that blocks bad actions.

4. **Benchmark convergence**: Shows that the frontier for agent improvement is not always bigger models or better prompts, but better *state design*.

---

## Source

- **Paper**: [arXiv:2606.20529](https://arxiv.org/abs/2606.20529)
