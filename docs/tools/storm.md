# STORM: Multi-Perspective Wiki Generation

> Paper: [arXiv:2402.14207](https://arxiv.org/abs/2402.14207) · Stanford NLP, 2024  
> GitHub: [stanford-oval/storm](https://github.com/stanford-oval/storm)  
> Hosted: [storm.genie.stanford.edu](https://storm.genie.stanford.edu)

## TL;DR

STORM (Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking) researches a topic by simulating expert conversations from multiple perspectives before writing. Compared to retrieval-augmented baselines, STORM articles are **25% more organized** and **10% broader in coverage**, as rated by Wikipedia editors. Open source, supports any litellm-compatible model including Claude.

---

## The insight

The bottleneck in long-form article generation is not the writing — it's the *pre-writing*: understanding what questions to ask, what angles exist, and what sources to trust. STORM front-loads this research phase using a multi-agent simulation that mirrors how a Wikipedia editor approaches a new topic.

---

## How it works

### Step 1: Find diverse perspectives

STORM retrieves Wikipedia articles on similar topics and extracts the distinct perspectives each takes — the historical angle, the technical angle, the criticism angle, etc. It then instantiates a set of simulated "writer personas", one per perspective.

### Step 2: Simulate expert Q&A

Each writer persona poses questions to a simulated "topic expert" grounded on internet search results. The expert answers with citations. Multiple rounds of questions per perspective → broad, multi-angle source coverage before a word of the article is written.

### Step 3: Build an outline

The collected information is assembled into a structured outline. Only then does the LLM write the article sections, each grounded on the gathered sources.

---

## Results

Evaluated on FreshWiki (100 high-quality recent Wikipedia articles):

| Metric | STORM vs RAG baseline |
|--------|----------------------|
| Organized (editors) | +25% absolute |
| Broad coverage | +10% absolute |

Wikipedia editor feedback also surfaced new failure modes: source bias transfer (the model inherits slant from retrieved sources) and fact over-association (entities associated incorrectly because they co-occur in sources).

---

## Co-STORM: human in the loop

Co-STORM adds a collaborative mode where a human can join the expert Q&A simulation:

- **Multiple agent types**: expert agents, a moderator, a human participant
- **Turn management**: the system manages who speaks next
- **Dynamic mind map**: information is organised into a live hierarchical structure the human can inspect and redirect

Co-STORM is for deep-dive research where you want to steer the coverage interactively.

---

## Installation & usage

```bash
pip install knowledge-storm
```

Or clone and configure:

```bash
git clone https://github.com/stanford-oval/storm
cd storm
pip install -r requirements.txt

# Run with Claude (via litellm)
python examples/storm_examples/run_storm_wiki_claude.py \
  --output-dir ./output \
  --topic "Mixture of Experts in LLMs"
```

STORM integrates with all litellm-supported models, which includes Claude models via the standard Anthropic SDK path.

---

## Limitations

- Relies on internet search — quality depends on available sources for the topic
- Source bias transfer: retrieved pages can introduce slant into the article
- Fact over-association: co-occurrence in sources can create spurious connections
- Best for topics with existing web coverage; thin coverage → thin articles

---

## Related work

- [LEANN](leann.md) — for personal-scale RAG over your own documents
- [Hyper-Extract](hyper-extract.md) — structured knowledge extraction from documents

---

## Source

- **Paper**: [arXiv:2402.14207](https://arxiv.org/abs/2402.14207)
- **GitHub**: [stanford-oval/storm](https://github.com/stanford-oval/storm)
- **Try it**: [storm.genie.stanford.edu](https://storm.genie.stanford.edu)
