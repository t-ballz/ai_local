# Tapered Language Models: Free Perplexity via Non-Uniform Depth

> Source: [arXiv:2606.23670](https://arxiv.org/abs/2606.23670) · Jun 2026  
> Authors: Reza Bayat, Ali Behrouz, Aaron Courville

## TL;DR

Tapered Language Models (TLMs) progressively reduce layer width from input to output using a cosine schedule, allocating more capacity to early layers and less to late layers. Consistent perplexity improvements over uniform-width baselines across four architectures (Transformer, Gated Attention, Hope-attention, Titans) and multiple scales — with no additional compute. The authors call it "a free lever hidden in plain sight."

---

## The problem

Standard transformer (and hybrid) architectures use uniform layer width throughout the network — each layer has the same dimension. This is a default inherited from early design decisions, not an empirically validated optimum.

Prior work on early-exit models and layer importance analysis hints that early layers do more heavy lifting than late layers in language modeling. If true, giving all layers the same capacity wastes parameters in the back of the network.

---

## How it works

**Cosine tapering**: Layer width is reduced according to a cosine schedule from the input end to the output end. If the maximum width is $d_{max}$ and the minimum width is $d_{min}$, layer $l$ of $L$ total layers has width:

$$d_l = d_{min} + \frac{1}{2}(d_{max} - d_{min})\left(1 + \cos\!\left(\frac{\pi l}{L}\right)\right)$$

This allocates maximum capacity to the first layer, reduces smoothly, and reaches minimum width at the final layer.

**No additional compute**: Total parameter count is approximately preserved — the tapered model is not larger than the baseline, just differently distributed. Inference compute is unchanged.

**Architecture-agnostic**: Tested on Transformer, Gated Attention, Hope-attention, and Titans architectures — the benefit is consistent across all four.

---

## Results

Consistent perplexity improvements over uniform-width baselines at multiple scales, across all four tested architectures. No compute overhead.

---

## Why it matters for local AI

Tapered LMs are a free architectural improvement: same parameter count, same inference cost, better quality. Any architecture search or pretraining effort for local models should include tapering as a baseline to beat. The result also validates the hypothesis that early layers are more important — with implications for layer pruning and quantization (later layers can be compressed more aggressively).

---

## Limitations

- Perplexity improvements may not uniformly translate to downstream task performance — benchmark coverage beyond perplexity is limited
- Optimal taper schedule (cosine vs. linear vs. other) and min/max width ratio require tuning
- Evaluation at large scale (>10B parameters) not reported

---

## Source

- **Paper**: [arXiv:2606.23670](https://arxiv.org/abs/2606.23670)
- **Preprint date**: Jun 2026
