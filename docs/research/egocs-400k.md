# EgoCS-400K: Egocentric Gameplay Dataset for World Models

> Source: [arXiv:2606.18180](https://arxiv.org/abs/2606.18180) · June 2026  
> Authors: Rongjin Guo, Dong Liang, Yuhao Liu, Fang Liu, Tianyu Huang, Gerhard P. Hancke, Rynson W. H. Lau

## TL;DR

A 400K-video, 10K-hour egocentric dataset from Counter-Strike professional matches, fully annotated with player states, actions, game events, and camera motion. Bridges the gap between passive video datasets and **interactive world models** by providing video-action-language trajectories where the actions actually caused the observed future scenes.

---

## The world model training problem

Most video datasets are **passive** — a camera records what happens, but there's no record of what agent actions produced the observations. World models need to learn the transition function `(state, action) → next_state`, which requires:

1. Actions paired with outcomes
2. Rich state annotations (not just pixels)
3. Interactive diversity (the agent makes choices that branch the future)

EgoCS-400K provides all three, extracted from professional CS match replays where every frame has a complete game state record.

---

## Dataset statistics

| Metric | Value |
|--------|-------|
| Total videos | 400K+ |
| Total duration | 10,000 hours |
| Source matches | 1,000+ professional matches |
| Game rounds | 40,000+ |
| Maps | 13 |
| Player viewpoints per round | 10 |

---

## Annotations

Each video clip is annotated with:
- **Player states**: position, health, equipment, team
- **View direction and camera motion**: exact angles and movement
- **Keyboard/button inputs**: the actual actions taken
- **Weapon usage and game events**: kills, plant/defuse, round outcomes
- **Round-level context**: map, team composition, round number

This is richer than any prior gaming dataset — the replay system gives access to ground-truth state that would be invisible from pure video.

---

## Supported tasks

| Task | What it tests |
|------|--------------|
| Action-conditioned future prediction | Can the model predict next frames given the action? |
| State- and event-aware scene rollout | Does the model track game state across the rollout? |
| Replay-grounded captioning | Can the model describe what happened and why? |
| Egocentric action understanding | Can the model classify what action was taken? |

---

## Why Counter-Strike

- **Dense actions**: CS players act every frame — high signal density
- **Rich state**: replay system captures complete hidden state (not just visible pixels)
- **Professional quality**: consistent, high-skill play avoids degenerate behaviors
- **Egocentric**: first-person perspective matches embodied AI training needs
- **Interactive**: player decisions genuinely branch the future — not a scripted scenario

---

## Source

- **Paper**: [arXiv:2606.18180](https://arxiv.org/abs/2606.18180)
