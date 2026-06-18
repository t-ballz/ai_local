# Research & Articles

Papers and articles on AI/ML topics beyond local inference — training methods, algorithms, and findings worth understanding.

| Paper / Article | Topic | Date |
|-----------------|-------|------|
| [Scaling Self-Play with Self-Guidance (SGS)](sgs-self-play.md) | Synthetic data generation, theorem proving | Apr 2026 |
| [Dive into Claude Code](dive-into-claude-code.md) | AI agent architecture, harness design patterns | Apr 2026 |
| [Recursive Language Models (RLMs)](recursive-language-models.md) | Long-context via recursive REPL decomposition; no context rot | Dec 2025 |
| [Synthetic Data for any Differentiable Target (DPG)](dataset-policy-gradient.md) | RL-optimised data generation; encodes QR codes into model weights via benign text | Apr 2026 |
| [Memory is Reconstructed, Not Retrieved (MRAgent)](graph-memory-agents.md) | Active graph-traversal memory for agents; +23.3% LoCoMo, 5× fewer tokens than A-Mem | Jun 2026 |
| [HarnessX: Evolvable Agent Harnesses](harnessx.md) | Auto-adapting agent scaffolds via AEGIS pipeline; +14.5% avg, +5% with model co-evolution | Jun 2026 |
| [PoLar: Program-of-Layers](polar-program-of-layers.md) | Per-input skip/repeat of layer segments; +3.8–5.8% accuracy, often with less compute | ICML 2026 |
| [SeeRepo: Visual Dependency Graphs for Code Agents](seerepo.md) | Visual repo maps at fault-localization stage; −25% tokens, −26% cost on SWE-bench | Jun 2026 |
| [From Chatbot to Digital Colleague](chatbot-to-digital-colleague.md) | Workspace + Skill paradigm as the decisive transition to persistent autonomous agents | Jun 2026 |
| [From AGI to ASI](from-agi-to-asi.md) | Google DeepMind framework: four pathways, five bottlenecks, why forecasting AI progress is itself a field | Jun 2026 |
| [S2L-PO: Smaller Models as Explorers in GRPO](s2l-po-grpo-diversity.md) | Frozen small-model rollouts for policy-level diversity; +8.8% AIME24 training an 8B with a 1.7B | 2025 |
| [VibeThinker-3B: Frontier Reasoning at 3B](vibethinker-3b.md) | 94.3 AIME26 / 80.2 LiveCodeBench from a 3B model via curriculum SFT + RL + self-distillation | Jun 2026 |
| [MiniMax Sparse Attention](minimax-sparse-attention.md) | 28.4× fewer attention ops at 1M context; 14.2× prefill speedup; ships in MiniMax-M3 (109B) | Jun 2026 |
| [FlashMemory-DeepSeek-V4: Lookahead Sparse Attention](flashmemory-deepseek-v4.md) | Proactive KV cache prediction compresses cache to 13.5% at 500K context; +0.6% accuracy | Jun 2026 |
| [Attention Amnesia in Hybrid LLMs](attention-amnesia-hybrid-llms.md) | CoT-SFT destroys long-context recall (67% → 9%) in hybrid models; QK-Restore fixes it without retraining | Jun 2026 |
| [N-GRPO: Semantic Neighbor Mixing](n-grpo.md) | Manifold-constrained embedding diversity for GRPO; no second model needed; consistent math reasoning gains | Jun 2026 |
| [NextLat: Next-Latent Prediction](nextlat.md) | Auxiliary latent-state prediction injects world-model bias into transformers; 3.3× self-speculative decoding speedup | Nov 2025 |
| [Agentic Automata Learning](agentic-automata-learning.md) | Agents reconstruct hidden DFAs via membership/equivalence queries; clean benchmark for world-model claims | Jun 2026 |
| [ExpRL: Dense RL for LLM Mid-Training](exprl-mid-training.md) | LLM-judge process+outcome rewards during mid-training; better RL priming than SFT, GRPO, or self-distillation | Jun 2026 |
| [Can LLMs Discover Zero?](llm-discover-zero.md) | Seeing the token `0` ≠ knowing the concept; models need explicit relational examples; language pretraining halves the required count | Jun 2026 |
| [Beyond LoRA: PEFT Method Comparison](peft-beyond-lora.md) | OFT beats LoRA on image gen (lower VRAM + better fidelity); Lily edges LoRA on math; don't default to LoRA | Jun 2026 |
| [Agentic Benchmarking of Open Models](agentic-benchmarking-open-models.md) | Skill docs help large models, break small ones; Qwen3-14B: 100%→0% when CLI docs added; introduces Markers framework | Jun 2026 |
| [d-OPSD: Self-Distillation for Diffusion LLMs](dopsd-diffusion-llm-distillation.md) | On-policy self-distillation adapted for dLLMs via suffix conditioning + step-level supervision; 10× compute savings vs RLVR | Jun 2026 |
| [ZPPO: Teacher in Prompts, Not Gradients](zppo.md) | Knowledge distillation via BCQ/NCQ prompt strategies; replay buffer keeps student in zone of proximal development; beats GRPO on 31 benchmarks | Jun 2026 |
| [OPD-Evolver: Self-Evolving Agents](opd-evolver.md) | Dual-loop agent: fast memory hierarchy at test time, slow distillation offline; 9B competes with 397B models | Jun 2026 |
| [Efficient Attention in Hybrid Architectures](efficient-attention-hybrid-architectures.md) | Efficient attention is an optimization prior, not storage; large-window laziness delays retrieval heads; apply NoPE to full-attention layers | Jun 2026 |
| [UniAR: Unified Multimodal Autoregressive](uniar-unified-multimodal.md) | Single discrete visual tokenizer bridges understanding + generation; SOTA image gen/editing; ICML 2026 | Jun 2026 |
| [ActWorld: Interactive World Model Memory](actworld-interactive-world-model.md) | Hierarchical action-aware memory routes compression by interaction significance; 2× success on object manipulation | Jun 2026 |
| [ACE-Ego-0: Human+Robot Data for VLA](ace-ego-0.md) | Converts human egocentric videos to robot pseudo-trajectories; reliability-aware training; SOTA on RoboCasa + RoboTwin | Jun 2026 |
| [EgoCS-400K: Gameplay Dataset for World Models](egocs-400k.md) | 400K videos / 10K hours from CS professional matches; dense action-state-event annotations for interactive world model training | Jun 2026 |
| [Self-Evolving Visual Questioner](self-evolving-visual-questioner.md) | VLMs bootstrap harder visual questions via propose→rewrite→filter→retrain loop; no external supervision; backbone-agnostic | Jun 2026 |
