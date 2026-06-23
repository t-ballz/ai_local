# MCompassRAG: Topic Metadata for Efficient Paragraph-Level Retrieval

> Source: [arXiv:2606.18508](https://arxiv.org/abs/2606.18508) · June 2026  
> Authors: Amirhossein Abaskohi, Raymond Li, Gaetano Cimino, Peter West, Giuseppe Carenini, Issam H. Laradji  
> Institution: University of British Columbia, University of Salerno, ServiceNow Research

## TL;DR

MCompassRAG enriches coarse-grained document chunks with topic-level metadata and trains a lightweight retriever via LLM-teacher distillation to guide retrieval. The approach achieves 8.24% improvement in information efficiency over dense retrieval baselines while maintaining 5× lower latency than strong LLM-based RAG methods, solving the fundamental granularity trade-off in RAG.

---

## The problem

Retrieval-augmented generation systems face a critical granularity trade-off: fine-grained chunks (sentences, short paragraphs) improve retrieval precision but dramatically expand the search space, increasing latency and indexing cost. Larger chunks reduce the search space but mix multiple topics into a single embedding, introducing semantic noise where relevant evidence gets diluted by unrelated text and partially relevant chunks are over-retrieved.

This trade-off becomes especially limiting in deep research tasks where systems must perform many retrieval calls across large, heterogeneous corpora while maintaining both speed and precision. Existing solutions—proposition-level decomposition, hierarchical indexing, adaptive chunking—either require fine-grained preprocessing and additional indices, or add LLM-based re-ranking stages that introduce expensive inference-time latency.

The core question: how can we make coarse-grained chunks searchable without adding extra preprocessing stages or inference-time LLM calls?

---

## Approach: Topic-aware metadata guidance with knowledge distillation

MCompassRAG uses a three-component strategy:

### 1. Metadata enrichment

Each document chunk is processed through a topic model (CEMTM—a Qwen3-Embedding-based topic model) to generate:
- **Chunk-topic distributions**: Sparse representations capturing which topics are present in each chunk
- **Topic centroid embeddings**: Embedding-space representatives of each topic (K=100 topics, trained on WikiWeb2M)

These are cached in a corpus-level metadata bank and don't require additional indices or search overhead.

### 2. Query-side metadata selection and abstraction

At inference time, rather than relying only on cosine similarity between query and chunk embeddings:
1. The base query is encoded using a lightweight Qwen3-Embedding-4B encoder
2. A **selection policy** compares the query embedding against all metadata entries to identify the top topic signals most relevant to the query
3. An **abstraction module** summarizes the selected metadata distributions into a compact query-topic vector, reducing noise from any single metadata signal
4. This query-topic vector is concatenated with the query embedding to form the metadata-enriched query representation

### 3. Lightweight student retriever via LLM-teacher distillation

Training uses an extreme multi-label classification objective with knowledge distillation:
- **Teacher**: Qwen3-32B LLM with query expansion and topic-aware scoring (used only during training)
- **Student**: Lightweight MLP classifier trained on BCE (binary cross-entropy) and knowledge distillation losses to identify relevant chunks from metadata-enriched representations
- **Inference**: Only the student is used—no LLM calls needed at serving time

The framework is topic-model-agnostic: any topic model whose embeddings live in the retriever's semantic space can be used.

---

## Key results

**Retrieval performance** (Information Efficiency, Precision, Recall across six benchmarks):

- **DRBench (multi-hop research)**: IE of 47.97 vs. 37.47 for the strongest non-LLM baseline (SAKI-RAG)—**28% IE improvement** on the hardest benchmark
- **LegalBench-RAG**: Leads on all three retrieval metrics
- **Average across six benchmarks**: +8.24% information efficiency improvement over strongest non-LLM baseline
- **Latency**: 5× lower latency than strong LLM-based RAG baselines

**Downstream task performance** (F1, ROUGE-L, BERTScore on HotpotQA, SQuAD, Dragonball, LongBenchV2):

- Competitive with or exceeding strong baselines including RAPTOR, ReflectiveRAG, DF-RAG, and PageIndex
- Maintains generation quality while dramatically improving retrieval efficiency
- Demonstrates the gains are not solely due to model scale—even with AllMiniLM-L6-V2 encoder, MCompassRAG remains competitive with baselines using Qwen3-Embedding-4B

**Benchmarks evaluated**: SCI-DOCS, LegalBench-RAG, Dragonball, HotpotQA, SQuAD, DRBench, LongBenchV2

---

## Why it matters

1. **Solves the chunking granularity dilemma**: Enables coarse-grained indexing (efficiency) without sacrificing precision through metadata enrichment rather than additional indices
2. **Inference-efficient**: No extra LLM calls, no hierarchical retrieval stages, no expensive reranking—only lightweight metadata selection and student MLP scoring
3. **Modular and agnostic**: Works with any topic model; distillation approach preserves teacher quality while eliminating inference-time LLM dependency
4. **Especially strong on multi-hop reasoning**: Largest gains on research-heavy benchmarks like DRBench where documents contain mixed topics and multiple hops are required
5. **Practical for production systems**: The 5× latency reduction while improving quality makes this immediately valuable for high-volume RAG applications

---

## When to use this

- **Best for**: Large-scale RAG systems over heterogeneous document collections where latency is critical and multi-hop or research-heavy reasoning is required
- **Setup cost**: Requires pre-computing topic models over the corpus and training a lightweight student retriever on task-specific data (using synthetic labels if needed)
- **Prerequisites**: 
  - Topic model that can embed topics in your retriever's semantic space (the paper uses CEMTM on Qwen3-Embedding)
  - At least some retrieval supervision data or synthetic query-chunk pairs for distillation
- **Avoid if**: Your chunks are already very fine-grained (e.g., sentence-level) or your documents are highly homogeneous—the metadata guidance will be less beneficial
- **Complements**: Query expansion, iterative retrieval, reranking, and context compression—MCompassRAG is orthogonal to post-retrieval filtering or generation-side optimizations

---

## Source

- **Paper**: [arXiv:2606.18508](https://arxiv.org/abs/2606.18508)
- **Code**: [GitHub: AmirAbaskohi/MCompassRAG](https://github.com/AmirAbaskohi/MCompassRAG)
- **Topic model**: CEMTM (Abaskohi et al., 2025)
- **Embedding models**: Qwen3-Embedding-4B (retriever), Qwen3-32B (LLM teacher)
