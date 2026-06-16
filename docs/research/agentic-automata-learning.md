# Agentic Automata Learning: Benchmarking Agent World Models

> Source: [arXiv:2606.16576](https://arxiv.org/abs/2606.16576) · June 2026

## TL;DR

"World model" claims about agents are usually untestable vibes. This paper makes them gradeable: an agent must reconstruct a hidden **deterministic finite automaton (DFA)** by interacting with an oracle through membership and equivalence queries — the same framing used in classical automata learning theory. Reasoning models do meaningfully better than base models, but everything degrades sharply as the automaton grows, and all LLMs lag well behind classical algorithms.

---

## The task

A hidden DFA defines a language (a set of strings). The agent cannot see the automaton — only query an oracle:

- **Membership query**: "Does this string belong to the target language?" → yes/no
- **Equivalence query**: "Is this my hypothesised DFA the correct one?" → yes, or a counterexample string

The agent's goal is to reconstruct the target DFA using as few queries as possible. Classical algorithms (L*, TTT) serve as strong, well-understood baselines — unlike most agent benchmarks where the baseline is another LLM.

The task complexity is controlled by the number of DFA states — larger DFAs require longer, more structured reasoning chains.

---

## Why this is a good benchmark

Most agent "world model" evaluations ask whether an agent produces plausible outputs. This benchmark asks whether the agent is actually modelling its environment:

| Property | What it enables |
|----------|----------------|
| Hidden structure | Agent must infer, not observe |
| Verifiable answer | The DFA is either correct or not |
| Scalable complexity | DFA size directly controls difficulty |
| Classical baselines | Algorithmic lower bounds on query efficiency |
| Interaction efficiency measurable | Count queries, not just final accuracy |

---

## Key results

- Performance degrades substantially as DFA size increases — no model maintains accuracy at high complexity
- **Reasoning models significantly outperform standard models** — the structured query-plan-hypothesis loop aligns well with chain-of-thought reasoning
- **All LLMs lag far behind classical algorithms** in robustness and query efficiency
- Failure modes cluster around: poor query planning, failed evidence synthesis across query history, and premature hypothesis commitment

---

## Implications for agent evaluation

The result that reasoning models outperform base models is interpretable: actively reconstructing a hidden structure through strategic queries is exactly what long chain-of-thought is designed for. The result that all models degrade with size means current LLMs are partially modelling their environment — enough to beat random, not enough to rival principled search.

For anyone benchmarking agent "world model" claims: this is a clean, controlled, theoretically-grounded test that doesn't require a live environment or subjective scoring.

---

## Source

- **Paper**: [arXiv:2606.16576](https://arxiv.org/abs/2606.16576)
