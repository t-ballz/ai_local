# Every System is a Log

> Source: [Restate blog](https://www.restate.dev/blog/every-system-is-a-log-avoiding-coordination-in-distributed-applications) · 2026

## TL;DR

Databases, message queues, coordination services, and state machines are all fundamentally log-shaped. Once you see this, a surprising consequence follows: if you route all state changes through *one* shared event journal, most distributed coordination problems dissolve — not by solving them, but by making them structurally impossible.

---

## Everything is already a log

| System | How it's a log underneath |
|--------|--------------------------|
| Kafka, Pulsar, RabbitMQ | Distribute the log abstraction directly |
| Relational databases | Built on a write-ahead log; the WAL *is* the source of truth |
| ZooKeeper, etcd | Implement Raft/Paxos consensus logs at their core |
| State machines | Are just materialised views of a log of transitions |

The classic formulation: **"the log is the database; everything else is cache."** Tables, indexes, read replicas — all derived. The log is primary.

---

## The coordination problem

A payment handler that touches fraud detection, account state, and a notification queue faces the classic distributed systems nightmare:

- Partial failures: step 3 completes, then step 4 crashes
- Phantom updates: a retry re-runs step 3 and charges twice
- Race conditions: two concurrent handlers read the same account balance before either writes
- Lock hazards: acquiring a distributed lock shifts the problem rather than solving it (fencing tokens, lost-lock scenarios)

The instinct is to add locks and idempotency keys to each system independently. This distributes the coordination burden across N systems, each with its own failure mode.

---

## The log insight

If every operation — fraud check, lock acquisition, account update, notification enqueue — **appends to a single shared event journal**, then:

1. There is one linear history of events. No two operations can interleave ambiguously.
2. A retried handler receives its full execution journal. It detects already-completed steps and skips them automatically.
3. Lock acquisition is just a conditional append. Race conditions between two handlers trying to lock the same key become a serialisation question the log already answers.

> "Having a single place (the one log) that forces a linear history of events as the ground truth eliminates the need to synchronise across systems."

There is nothing to coordinate *because coordination is already implicit in the log's total order*.

---

## Scope matters

The log shouldn't govern all architecture-wide state — just state **scoped to a handler or service**. Keeping the blast radius small preserves service isolation while still eliminating intra-handler coordination.

---

## Restate: the practical implementation

[Restate](https://restate.dev) is an open-source durable execution broker that materialises this pattern. Its SDK gives handlers:

- `ctx.run()` — durably executes an action and stores the result in the execution journal; retries skip already-completed steps
- **Virtual Objects** — handlers that automatically lock a key and access scoped state
- **Exactly-once delivery** between handlers
- **Idempotency keys and persistent timers**, all log-backed

The result: queues, databases, locks, and schedulers collapse into one dependency.

*Note: Restate is currently single-node; distributed versions are forthcoming.*

---

## Why this matters for AI systems

Agent frameworks face an almost identical problem: multi-step tool invocations with partial failures, retries that must not re-execute side effects, and concurrent agents racing on shared state. The log-as-foundation pattern is exactly what durable execution frameworks (Restate, Temporal, Inngest) apply to make agents resumable and exactly-once by construction — rather than by careful per-step idempotency wiring.

---

## Source

- **Article**: [Every System is a Log — Avoiding Coordination in Distributed Applications](https://www.restate.dev/blog/every-system-is-a-log-avoiding-coordination-in-distributed-applications)
- **Restate**: [restate.dev](https://restate.dev) · [GitHub](https://github.com/restatedev/restate)
