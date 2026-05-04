# How LLMs Work

> A practical overview of the architecture and training pipeline behind generative large language models.

## TL;DR

A generative LLM is a **decoder-only Transformer** trained to predict the next token given all previous tokens. At inference time it repeats that prediction step sequentially — one token at a time — to produce text. Almost every model covered in this wiki (Llama, Qwen, Mistral, Gemma, DeepSeek, SmolLM) is this class of model.

---

## Tokenization

Before any computation happens, raw text is split into **tokens** — subword fragments, not necessarily whole words. A tokenizer such as BPE (Byte Pair Encoding) or SentencePiece learns a fixed vocabulary (typically 32K–128K tokens) where common words are a single token and rare words are split into multiple pieces.

```
"unhappiness" → ["un", "happiness"]   # 2 tokens
"cat"         → ["cat"]               # 1 token
" 2025"       → [" 2025"]             # 1 token
```

The model never sees characters or bytes directly — only integer token IDs. All sizing (context length, VRAM usage) is in tokens, not characters or words.

---

## The Transformer Layer

Every modern LLM stacks N identical layers. Each layer has two sub-blocks with a **residual connection** around each:

```
Input
  └─▶  Self-Attention  ──(+ residual)──▶  Layer Norm
  └─▶  Feed-Forward Network (FFN)  ──(+ residual)──▶  Layer Norm
       ▼
     Output (same shape as input)
```

Residual connections let the gradient flow backwards through many layers without vanishing, enabling models to go very deep (32–128 layers in typical LLMs).

---

## Self-Attention

Self-attention is what lets every token look at every other token in the context and decide how much each one matters.

For each token, the layer projects its embedding into three vectors:

| Vector | Role |
|--------|------|
| **Query (Q)** | "What am I looking for?" |
| **Key (K)** | "What do I contain?" |
| **Value (V)** | "What do I output if attended to?" |

Attention scores are computed as:

```
Attention(Q, K, V) = softmax( Q·Kᵀ / √dₖ ) · V
```

The division by √dₖ (square root of key dimension) prevents the dot products from growing too large, which would collapse the softmax into near-zero gradients.

**Multi-head attention** runs this process H times in parallel (H = 8, 16, 32, … depending on model size), each head learning to attend to different relationships. Outputs from all heads are concatenated and projected back to the model dimension.

**Causal masking** — generative (decoder-only) models cannot attend to future tokens. A triangular mask is applied so each token only sees tokens at or before its position.

---

## Positional Encoding

Transformers have no built-in notion of order — without it, "cat sat on mat" and "mat on sat cat" would look identical. Positional information is injected by adding a position-dependent signal to each token embedding.

| Method | Used by |
|--------|---------|
| Sinusoidal (original) | Original Transformer |
| Learned absolute | GPT-2, early BERT |
| **RoPE** (Rotary Position Embedding) | Llama, Qwen, Mistral, Gemma, most modern LLMs |
| ALiBi | Some older models |

RoPE encodes position by rotating the Q and K vectors; it generalises better to lengths beyond training context than earlier methods and is now the de-facto standard.

---

## Feed-Forward Network (FFN)

After attention, each token position is processed independently through a small MLP:

```
FFN(x) = activation( x·W₁ + b₁ )·W₂ + b₂
```

Modern models use **SwiGLU** or **GeGLU** activations instead of ReLU, which improves training stability and quality. The FFN dimension is typically 4× the model dimension (e.g. d_model=4096, FFN=16384), making it the largest component by parameter count in a dense model.

---

## Pre-training

Pre-training is the phase that gives the model its general knowledge and language ability. The objective is simple: **predict the next token**.

Given a large corpus of text (trillions of tokens scraped from the web, books, code, etc.), the model is trained to maximise the probability of each token given everything before it:

```
Loss = -Σ log P(token_t | token_1, …, token_{t-1})
```

This is **causal language modelling** (CLM), also called autoregressive training. No human labels are needed — the data itself is the supervision.

Pre-training for frontier models uses thousands of GPUs for weeks to months and costs millions of dollars. Open-weight models publish the trained weights so you never have to repeat it.

---

## Context Window and KV Cache

The **context window** is the maximum number of tokens the model can attend to in a single forward pass — everything earlier is invisible to it.

| Model family | Typical context |
|-------------|-----------------|
| Early GPT-2 | 1K tokens |
| Llama 3.x / Qwen3 / Mistral | 128K tokens |
| Llama 4 Scout | 10M tokens |

During generation, the model computes K and V matrices for every token it has seen. Recomputing these from scratch each step would be O(n²) per token. The **KV cache** stores those matrices and reuses them, so each new token only costs O(n) attention operations. The downside: the cache grows linearly with context length and consumes significant VRAM. At long contexts, KV cache often dominates memory more than the weights themselves.

!!! note "Why long context is expensive"
    A 70B model at FP16 weights takes ~140 GB. Its KV cache at 128K tokens can add another 50–100 GB depending on the number of heads and layers.

---

## Inference and Sampling

The model produces a **logit** for every token in its vocabulary at each step. A softmax converts these to a probability distribution, and a decoding strategy picks the next token.

| Strategy | Description |
|----------|-------------|
| **Greedy** | Always pick the highest-probability token. Deterministic, but repetitive. |
| **Temperature** | Scale logits by 1/T before softmax. T < 1 → sharper (more focused); T > 1 → flatter (more random). |
| **Top-k** | Sample only from the k highest-probability tokens. |
| **Top-p (nucleus)** | Sample from the smallest set of tokens whose cumulative probability ≥ p (e.g. p=0.9). |
| **Min-p** | Exclude tokens below a fraction of the top token's probability. Newer alternative to top-p. |

In practice, temperature + top-p (or min-p) are the most common combination. Temperature=0 collapses to greedy decoding.

---

## Fine-tuning

Pre-trained models are good at continuing text but poor at following instructions. Fine-tuning steers the model's behaviour using smaller, curated datasets.

**Supervised Fine-Tuning (SFT)**
The model is trained on (prompt, response) pairs with the same next-token-prediction loss, but only the response tokens are included in the loss. This teaches instruction-following format.

**RLHF (Reinforcement Learning from Human Feedback)**
Human annotators rank model outputs. A separate reward model learns to score outputs, and the LLM is updated via RL (typically PPO) to increase reward. Used in ChatGPT, Claude, Gemma instruct variants.

**DPO (Direct Preference Optimization)**
A simpler alternative to RLHF that uses preference pairs (chosen vs rejected response) directly in a supervised loss, without a separate reward model. Widely used in open models because it is more stable to train.

!!! tip "What 'Instruct' means in a model name"
    A model labelled `Llama-3.3-70B-Instruct` or `Qwen3-14B` (without `-base`) has gone through SFT and/or RLHF/DPO on top of the base pre-trained weights.

---

## Quantization

Model weights are normally stored as **bfloat16** (2 bytes per parameter). Quantization maps those values to lower-precision integers to reduce VRAM and memory bandwidth:

| Format | Bytes/param | Size of a 7B model |
|--------|-------------|-------------------|
| BF16 | 2.0 | ~14 GB |
| Q8_0 | ~1.0 | ~7 GB |
| Q4_K_M | ~0.5 | ~4 GB |
| Q2_K | ~0.25 | ~2 GB |

**GGUF** (the format used by llama.cpp, Ollama, LM Studio) packages quantized weights alongside the tokenizer and config in a single file. Quantization level names encode the method and variant — `Q4_K_M` means 4-bit, K-quant method, medium variant (a mix of 4-bit and 6-bit for key layers).

Quality degrades gradually: Q8 is nearly lossless, Q4_K_M shows minor degradation on hard tasks, Q2 is noticeably weaker. For most use cases Q4_K_M or Q5_K_M is the sweet spot.

---

## Dense vs. Mixture of Experts (MoE)

In a **dense** model every parameter is used for every token. Scaling means more compute per token proportional to parameter count.

In a **Mixture of Experts (MoE)** model, each Transformer layer replaces the single FFN with N parallel "expert" FFNs plus a small **router** network. The router selects top-k experts (typically 2) per token; only those experts activate.

```
Dense FFN:   every token → one FFN of size d_ffn
MoE FFN:     every token → router picks 2 of 16 experts, each 1/16 the size
```

| Property | Dense | MoE |
|----------|-------|-----|
| Active params per token | = Total params | << Total params |
| Total params (VRAM) | = Active params | >> Active params |
| Inference speed | Proportional to total | Fast (only active experts run) |
| Examples | Llama 3.x, Gemma 3, SmolLM3 | Llama 4 Scout, DeepSeek V3, Qwen3 (some) |

!!! note "MoE VRAM trap"
    All expert weights must reside in memory even though only 2 activate per token. A model listed as "17B active / 109B total" needs VRAM for 109B parameters.

---

## Further Reading

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — original Transformer paper (Vaswani et al., 2017)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — visual walkthrough by Jay Alammar
- [HuggingFace LLM Course](https://huggingface.co/learn/llm-course/chapter1/4) — hands-on introduction
