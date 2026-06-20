# Holo-World: Unified Camera, Object and Weather Control for Video World Model

> Source: [arXiv:2606.20083](https://arxiv.org/abs/2606.20083) · June 2026  
> Authors: Xiangchen Yin, Wenzhang Sun, Jiahui Yuan, Zijie Liu, Yinda Chen, Wei Li, Dachun Kai, Chunfeng Wang, Xiaoyan Sun

## TL;DR

Holo-World is a unified video world model that controls **camera movement, object position, and weather** simultaneously from a single starting image. It introduces the Unified Scene Adapter to factorize scene preservation and weather transfer into separate parameter spaces, enabling fine-grained multi-aspect control while maintaining scene structure and consistency.

---

## The problem

Video world models traditionally handle controls in isolation:
- Camera and object motion control exist separately from environmental state changes
- Weather generation depends on source videos or reconstructed scenes that already specify future structure
- No unified framework exists for controlling multiple aspects (camera, objects, weather) from a single image while preserving scene consistency

Holo-World addresses the **first-frame-anchored source-to-state** problem: starting from a single image, generate videos that either preserve the source world or transfer it to a target weather state, while following explicit camera and object motion controls.

---

## HoloStateData dataset

To enable unified control, the authors build **HoloStateData**, a state video dataset that:
- Transforms diverse videos into unified control samples
- Provides supervision signals for **camera**, **object**, and **weather** simultaneously
- Enables learning of factorized, controllable scene representations

---

## Unified Scene Adapter

The core innovation factorizes scene preservation and weather transfer into **distinct parameter subspaces**:

### Scene preservation pathway
- Uses **rendered background** to maintain static scene structure
- Applies **geometry buffers** for precise spatial control
- Incorporates **object controls** to track moving entities while preserving structure

### Weather transfer pathway
- Models **weather-dependent appearance changes** (lighting, colors, atmosphere)
- Handles **particle effects** (rain, snow, fog) specific to target weather conditions
- Operates in a separate parameter space from scene structure, avoiding interference

This factorization allows the model to transfer weather state without distorting camera framing or object positions.

---

## Scene-Weather Decomposed CFG

A classifier-free guidance (CFG) variant that:
- Guides **scene and weather residuals separately**
- Strengthens target weather effects without over-amplifying the full condition
- Prevents unwanted entanglement between scene structure and appearance changes

---

## Key results

Quantitative and qualitative experiments demonstrate:
- **Precise camera and object control** maintained across generated frames
- **Consistent scene structure** under diverse weather transfers
- **Outperforms video-to-video weather editing baselines** on weather-state generation
- Successfully transfers single-image scenes to rain, snow, night, and other weather conditions while respecting camera/object motion

---

## Why it matters

Holo-World addresses a real gap in video synthesis: most prior work either controls motion *or* environment, but not both. This work enables:

1. **Fine-grained scene editing** — change weather without losing camera control or object trajectories
2. **Single-image-anchored generation** — no need for reference videos or pre-computed scene reconstructions
3. **Practical applications** — virtual production, data augmentation for weather robustness, interactive video editing

The factorization approach (separating structure from appearance) is a general principle that could extend to other environmental controls beyond weather.

---

## Source

- **Paper**: [arXiv:2606.20083](https://arxiv.org/abs/2606.20083)
- **Project Page**: https://xiangchenyin.github.io/Holo-World/
- **Code**: https://github.com/XiangchenYin/Holo-World
