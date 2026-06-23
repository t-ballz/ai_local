# CUGA: Configurable Universal Generative Agent

> Source: [Hugging Face Blog](https://huggingface.co/blog/ibm-research/cuga-apps) · IBM Research · 2024–2026  
> GitHub: [cuga-project/cuga-agent](https://github.com/cuga-project/cuga-agent) · PyPI: `pip install cuga`  
> Home: [cuga.dev](https://cuga.dev)

## TL;DR

CUGA is a lightweight, open-source agent harness from IBM Research that handles orchestration, planning, and execution loops for agentic applications. It emphasizes simplicity: "the hard parts are handled, so your job is just the task." Supports any litellm-compatible model including open-weight models, tool integration via OpenAPI/MCP/LangChain, and multi-agent delegation. Includes 24 working example applications and ranks #1 on AppWorld and WebArena benchmarks.

---

## The insight

Building agentic applications requires solving two problems: (1) **the tool problem** — integrating APIs, managing state, handling errors; and (2) **the task problem** — defining what the agent actually does. CUGA solves the tool problem so you only have to solve the task problem. Tools return a standard response shape (`{"ok": true, "data": ...}` or `{"ok": false, "code": "...", "error": "..."}`), and the framework handles the rest.

---

## What it is

CUGA is a Python harness that wraps your LLM of choice and:

- **Handles orchestration** — planning loops, variable management, tool calls, code execution
- **Catches planning errors** — state reflection to detect and correct mistakes without re-deriving
- **Manages tool integration** — OpenAPI specs, MCP (Model Context Protocol) servers, LangChain functions, custom Python functions
- **Enables multi-agent patterns** — supervisor delegation, agent-to-agent communication, playbook-driven skills

The core API is minimal:
```python
agent = CugaAgent(model=..., tools=..., special_instructions=..., cuga_folder=...)
await agent.invoke(user_input)
```

---

## Key features

### Models & providers
- **Model agnostic**: OpenAI, Anthropic, IBM watsonx, LiteLLM, Ollama, open-weight models
- **Reasoning modes**: Fast, Balanced, Accurate — tradeoffs between latency and quality
- **Works with smaller models**: Benchmarks rank CUGA #1 on AppWorld and WebArena even when running against open-weight models like `gpt-oss-120b`

### Tool integration
- **OpenAPI**: automatic tool binding from OpenAPI specs
- **MCP servers**: 7 public MCP servers hosting 36 tools (web search, Wikipedia/arXiv lookup, geocoding, weather, finance, code analysis, text utilities)
- **LangChain**: direct integration of LangChain tools
- **CodeAct**: tool calls + generated Python code execution in sandboxed environments (local, Docker/Podman, or E2B cloud)

### Planning & execution
- **Long-horizon reasoning** — multi-step task decomposition with variable tracking
- **Self-correction** — state reflection detects planning errors and avoids re-derivation
- **Sandbox environments** — local execution, container isolation (Docker/Podman), or cloud sandbox (E2B)

### Governance & safety
- **Policy system** — six types: Intent Guards (block unsafe intents), Tool Approval (human-in-the-loop), Tool Guides (constrain tool use), Playbooks (task templates), Output Formatters, custom policies
- **Semantic matching** — policies triggered by keyword matching, not just function names
- **Human oversight** — approval workflows, audit trails

### Scaling patterns
- **CugaSupervisor** — multi-agent delegation and coordination
- **Agent-to-Agent (A2A)** — agents delegate to external specialist agents
- **Agent Skills** — playbook-driven knowledge reuse
- **ALTK-Evolve** — on-the-job learning and specialization

---

## Example applications (cuga-apps)

The **cuga-apps** repository includes 24 FastAPI applications, each demonstrating a different pattern:

### Research cluster
- **Paper Scout** — agentic paper discovery
- **Wiki Dive** — topic research and summarization
- **Web Researcher** — multi-source web research

### Productivity
- City briefings, travel planning, recipe generation, trail recommendations

### Document & media
- RAG (retrieval-augmented generation) over PDFs, audio transcripts, video

### Operations
- Live metrics monitoring and alerting

### Enterprise
- IBM product documentation advisor
- IBM Cloud architecture recommendations
- Multi-document policy compliance checking

### Multi-agent patterns
- **Ouroboros** — seven-agent lead-generation system with delegation

### Browser automation
- **Meetup Finder** — Playwright-based event discovery and scraping

---

## Installation & usage

```bash
pip install cuga
```

Then define tools and create an agent:

```python
from cuga import CugaAgent

tools = [
    {
        "name": "web_search",
        "type": "mcp",
        "endpoint": "https://mcp-server.example.com"
    }
]

agent = CugaAgent(
    model="claude-3-5-sonnet",  # or any litellm-compatible model
    tools=tools,
    special_instructions="You are a research assistant. Be thorough."
)

result = await agent.invoke("Research recent advances in diffusion models")
```

For OpenAPI tools, pass the spec directly:
```python
tools = [
    {
        "name": "weather_api",
        "type": "openapi",
        "spec": "https://api.weather.example.com/openapi.json"
    }
]
```

---

## Multi-agent example

Use CugaSupervisor to coordinate multiple agents:

```python
from cuga import CugaSupervisor

supervisor = CugaSupervisor(
    orchestrator_model="claude-3-5-sonnet",
    agents=[
        {"name": "researcher", "instructions": "Find and summarize sources"},
        {"name": "analyst", "instructions": "Extract insights from data"},
        {"name": "writer", "instructions": "Write articles"}
    ]
)

result = await supervisor.invoke("Write a comprehensive report on AI trends")
```

---

## Performance & benchmarks

CUGA ranks **#1 on AppWorld** (July 2025–February 2026) and **#1 on WebArena** (February 2025–September 2025) among agentic frameworks. Unlike frameworks that require frontier models, CUGA achieves these benchmarks with both proprietary and open-weight models.

---

## Production deployment

### Air-gapped deployment
Integrates with **IBM Sovereign Core** for isolated, compliant deployments:
- Agents run in transient, isolated containers within tenant infrastructure
- Boundary Isolation ensures no telemetry leaves the boundary
- Suitable for regulated environments (healthcare, finance, government)

### Public MCP server ecosystem
7 IBM-hosted public MCP servers on IBM Code Engine:
- Web search, Wikipedia, arXiv lookup
- Geocoding, weather data, financial data
- Code analysis utilities
- Text processing tools
- **No authentication required** — enables quick prototyping

---

## Why it matters

1. **Simplicity**: The orchestration problem is solved. You define the task, not the infrastructure.
2. **Flexibility**: Works with any LLM provider and any tool standard (OpenAPI, MCP, LangChain).
3. **Open-weight ready**: Proves that agentic systems don't require frontier models — open-weight models achieve competitive performance.
4. **Safety by default**: Governance policies are built in, not bolted on.
5. **Scalable patterns**: Multi-agent delegation, learning, and specialization are primitives, not afterthoughts.

---

## Limitations

- **Public MCP servers**: limited to 7 servers; larger deployments may need custom MCP infrastructure
- **Sandbox overhead**: CodeAct execution in containers adds latency compared to API-only tool use
- **Policy triggers**: semantic keyword matching is less precise than explicit intent parsing

---

## Related work

- [Strands Agents](strands-lerobot.md) — agent orchestration for robotics
- [STORM](storm.md) — multi-perspective research and article generation
- [LeRobot](strands-lerobot.md) — robotics datasets and policies

---

## Source

- **Blog**: [CUGA: Configurable Universal Generative Agent](https://huggingface.co/blog/ibm-research/cuga-apps)
- **GitHub**: [cuga-project/cuga-agent](https://github.com/cuga-project/cuga-agent)
- **Home**: [cuga.dev](https://cuga.dev)
- **Benchmarks**: [AppWorld](https://appworld-eval.github.io/), [WebArena](https://webarena.dev/)
