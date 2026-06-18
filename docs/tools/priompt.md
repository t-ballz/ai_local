# Priompt: Priority-Based Prompt Library

> Source: [GitHub — anysphere/priompt](https://github.com/anysphere/priompt)  
> License: MIT · npm: `@anysphere/priompt`

## TL;DR

Priompt is Cursor's open-sourced, JSX-based prompt library that handles **context window management automatically**. You assign a priority to every component of your prompt; when the token budget fills up, the renderer drops low-priority content first, keeping the highest-value context. Built for and battle-tested in a production code editor; 2.8k GitHub stars.

---

## The problem

LLM context windows are finite. In production agents and code editors, many pieces of information compete for the same space: recent conversation, tool output, background documentation, system instructions. The usual approach is ad-hoc string concatenation with manual truncation — fragile, hard to reason about, and impossible to tune without rewriting logic.

Priompt makes context budget an **explicit, declarative concern**.

---

## How it works

### Priority-based rendering

Every `<scope>` in a Priompt template carries a priority (`p` for absolute, `prel` for relative). The renderer finds the highest priority cutoff that fits all content within the token limit — high-priority scopes always survive; low-priority ones are dropped cleanly.

```tsx
import { scope, UserMessage, SystemMessage } from "@anysphere/priompt";

function MyPrompt({ recentHistory, backgroundDocs, query }) {
  return (
    <>
      <SystemMessage>
        <scope p={1000}>You are a helpful coding assistant.</scope>
      </SystemMessage>
      <scope p={500}>{backgroundDocs}</scope>   {/* drops first */}
      <scope p={900}>{recentHistory}</scope>    {/* preserved longer */}
      <UserMessage>{query}</UserMessage>
    </>
  );
}
```

In conversation history, later messages automatically receive higher priorities — recent context survives truncation.

### Key primitives

| Primitive | Purpose |
|-----------|---------|
| `<scope p={N}>` | Assign absolute priority; drops as a unit |
| `<scope prel={N}>` | Relative priority within parent scope |
| `<first>` | Fallback: use the first child that fits |
| `<isolate tokenLimit={N}>` | Hard token cap on a subsection |
| `<capture>` | Parse structured output back from the LLM response |
| `<empty tokens={N}>` | Reserve space for generation / tool output |

### Rendering

```ts
import { render } from "@anysphere/priompt";

const { prompt, tokenCount } = await render(<MyPrompt {...props} />, {
  tokenLimit: 8192,
  tokenizer: "cl100k_base",
});
```

---

## Installation

```bash
npm install @anysphere/priompt @anysphere/priompt-preview
```

The `priompt-preview` package gives a local dev UI for inspecting rendered prompts with live sourcemaps — useful for debugging what got dropped and why.

---

## Comparison to alternatives

| Library | Context management | Composability |
|---------|-------------------|---------------|
| LangChain / LlamaIndex | Manual truncation helpers | Object-based chains |
| DSPy | Optimizer-driven | Declarative signatures |
| **Priompt** | **Priority-based, automatic** | **JSX components** |

Priompt's edge is that it makes the *drop decision* a first-class, tunable property of the prompt structure — no post-hoc heuristics.

---

## Limitations

- TypeScript/JavaScript only — no Python port
- JSX syntax requires a TS/JS build step
- Efficient up to ~10K scopes; extreme fragmentation may slow rendering
- No built-in LLM client — purely a prompt construction library

---

## Source

- **GitHub**: [anysphere/priompt](https://github.com/anysphere/priompt)
- **npm**: `@anysphere/priompt`
