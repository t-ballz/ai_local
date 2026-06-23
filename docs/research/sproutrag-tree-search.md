# SproutRAG: Attention-Guided Tree Search with Progressive Embeddings

> Source: [arXiv:2606.18381](https://arxiv.org/abs/2606.18381) · June 2026  
> Authors: Amirhossein Abaskohi, Issam H. Laradji, Peter West, Giuseppe Carenini

## TL;DR

SproutRAG builds a semantic document hierarchy tree using learned inter-sentence attention patterns, enabling hierarchical RAG without expensive LLM calls during indexing or lossy summarization. Progressive embeddings improve as search narrows from coarse to fine granularity. Achieves 6.1% average information efficiency improvement across scientific, legal, and open-domain benchmarks.

---

## The problem

Retrieval-augmented generation systems face a fundamental trade-off: retrieving at coarse granularity (full documents) captures important context but may include irrelevant material; retrieving at fine granularity (sentences) identifies exact relevance but loses multi-sentence context and coherence. Existing approaches handle this poorly:

- **LLM-guided chunking**: Requires costly language model calls during indexing
- **Single-level context expansion**: Limited to one granularity level at retrieval time
- **Hierarchical summarization**: Loses information through compression

The core challenge: how can we build a hierarchical document structure that supports multi-granularity retrieval without external LLM calls, fixed expansion, or summarization-induced information loss?

---

## Approach: Attention-guided hierarchical tree with progressive embeddings

SproutRAG addresses this with a learned hierarchical structure and adaptive embeddings:

### 1. **Binary Chunking Tree Construction**
- Starts with sentence-level chunks as leaf nodes
- Uses **learned inter-sentence attention** from the retrieval model to identify which attention heads and layers best capture semantic document organization
- Progressively merges sentence chunks into progressively larger units (creating a binary tree structure)
- The tree structure itself is learned during training, not fixed or hand-crafted

Key insight: Attention weights naturally encode semantic relationships between sentences. By identifying the right attention heads/layers, the model learns which sentences belong together semantically.

### 2. **Progressive Embeddings**
Unlike models that fix embeddings for each chunk granularity level, SproutRAG learns embeddings jointly across all tree levels:

- Sentence-level embeddings are learned
- Parent nodes (merged chunks) develop their own embeddings through end-to-end training
- As the hierarchical beam search narrows from coarse to fine granularity, embeddings naturally progress through the tree
- No separate summarization or compression step needed—the model learns task-specific representations at each level

### 3. **Hierarchical Beam Search at Retrieval**
Given a query:
1. Start at the root or higher tree levels (coarse granularity)
2. Use beam search to retrieve top-k candidates at that level
3. Expand promising candidates to their children (finer granularity)
4. Progressively refine down to sentence-level chunks
5. This multi-granularity approach captures both relevance and multi-sentence coherence

### 4. **End-to-End Joint Training**
The entire framework—tree structure, embeddings, and retrieval objective—is trained jointly with a single loss function that optimizes both:
- Quality of embeddings across all granularity levels
- Quality of tree structure for capturing semantic organization

---

## Key results

**Quantitative performance:**
- **6.1% average information efficiency (IE) improvement** over the strongest baseline
- Evaluated across four benchmarks spanning scientific, legal, and open-domain settings

**Information efficiency metric:**
The paper measures information efficiency (IE), which evaluates how effectively the system retrieves relevant information while limiting unnecessary context—directly addressing the core RAG trade-off.

**Advantages over baselines:**
- No costly LLM calls during indexing (unlike LLM-guided chunking)
- Supports arbitrary multi-granularity retrieval (unlike fixed single-level expansion)
- Preserves information through learned embeddings (no summarization loss)
- Learns document structure end-to-end (rather than hand-crafted rules)

---

## Why it matters

This work addresses a critical pain point in practical RAG systems:

- **Scalable hierarchical RAG**: Many production RAG systems today either over-retrieve (coarse chunks with noise) or under-retrieve (fine chunks without context). SproutRAG enables principled multi-granularity retrieval without additional indexing overhead.

- **Learned structure over fixed rules**: Rather than imposing a predetermined tree structure (e.g., chapter → section → paragraph), SproutRAG's attention-guided approach learns the semantic organization that the model itself uses for retrieval. This is more flexible and transferable.

- **Efficient at scale**: By avoiding summarization and LLM calls at index time, the approach scales well to large document collections. Progressive embeddings avoid redundant computation at retrieval time.

- **Attention as structure discovery**: The insight that attention mechanisms encode document structure is valuable beyond RAG—it suggests that pre-trained attention patterns can be repurposed for structural understanding tasks.

---

## Related work

- **RAPTOR** and **GraphRAG**: Prior hierarchical RAG approaches using summarization or external graphs
- **Multi-granularity retrieval**: Other works exploring retrieval at multiple chunk sizes, but typically with fixed granularity levels or lossy compression
- **Environment-Aware IR**: Similar to [Environment-Aware IR: Retriever-Adaptive Queries](environment-aware-ir.md), recognizes that RAG components must be co-optimized rather than treated independently

---

## Source

- **Paper**: [arXiv:2606.18381](https://arxiv.org/abs/2606.18381)
- **Code**: [GitHub: AmirAbaskohi/SproutRAG](https://github.com/AmirAbaskohi/SproutRAG) (CC BY 4.0 license)
