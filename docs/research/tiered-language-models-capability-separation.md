# Tiered Language Models: Capability Separation in Open Weights

> Source: [arXiv:2606.21638](https://arxiv.org/abs/2606.21638) · Jun 2026  
> Authors: Charbel El Feghali, Arkil Patel, Nicholas Meade, Spandana Gella, Verna Dankers, Siva Reddy

## TL;DR

Tiered Language Models (TLMs) allow a single set of released model weights to support multiple capability tiers — a public version and one or more authorized versions with unlocked capabilities — via a compact secret key that modifies computation over identical weights. The public model is fully functional; the key unlocks additional languages, knowledge domains, or capabilities without changing the weights. Resistant to extraction attacks.

---

## The problem

Open-weight model release is binary today: you either release the full model (including all capabilities) or you don't. This creates a dilemma for labs that want to:

1. Release an open-weight model for research and deployment
2. Reserve certain capabilities (e.g. specific languages, regulated knowledge domains) for vetted or paying users
3. Comply with export controls or safety requirements that prohibit releasing certain capabilities publicly

Existing approaches (model watermarking, API access control) don't apply to local weights that users can run themselves.

---

## How it works

**Secret key mechanism**: A compact key (not an additional model) modifies the computation graph over the *same* weights. The key acts as a conditional adapter — it activates specific computation paths that are dormant in the keyless (public) version.

**Capability tiers**: Multiple keys can unlock different capability levels, supporting hierarchical tiers:
- **Public tier**: Full base functionality, no key required
- **Tier 1**: Key unlocks additional languages or knowledge
- **Tier 2**: Key unlocks specialized domain capabilities

**Extraction resistance**: The key is designed to resist extraction — an adversary with access to the public model cannot recover the key or the locked capabilities through black-box probing or weight analysis.

**Identical weights**: The public and authorized versions are the same GGUF/safetensors file — distribution is simplified and the authorized tier doesn't require a separate download.

---

## Results

The method works for unlocking new languages and specialized knowledge domains. Extraction attack resistance is demonstrated against standard probing methods.

---

## Why it matters for local AI

TLMs propose a path for labs to release open weights more liberally — knowing they can reserve sensitive capabilities — which could accelerate open-weight releases that would otherwise be withheld entirely. For local AI users, the implication is that future open-weight models might ship with a public tier plus optional capability unlocks, enabling a commercial open-weight ecosystem without API-only gatekeeping.

---

## Limitations

- Security of the key mechanism against sophisticated adversaries (white-box attacks, model inversion) is not fully established
- The capability separation boundary must be designed into training — retrofitting TLMs onto existing models may be difficult
- Key distribution and revocation infrastructure is an unsolved operational problem

---

## Source

- **Paper**: [arXiv:2606.21638](https://arxiv.org/abs/2606.21638)
- **Preprint date**: Jun 2026
