# LocateAnything-3B

> Source: [huggingface.co/nvidia/LocateAnything-3B](https://huggingface.co/nvidia/LocateAnything-3B) · NVIDIA

## TL;DR

NVIDIA's 3B-parameter Vision-Language Model for **visual grounding** — it takes an image and a natural-language query and returns bounding boxes for matched objects. Beats YOLO-class detectors on open-vocabulary tasks and GUI element grounding. Non-commercial licence (research/academic only).

---

## Model specs

| Property | Value |
|----------|-------|
| Parameters | 3B |
| Input | Images (up to 2.5K resolution) + text prompt |
| Output | Bounding boxes / point coordinates |
| Context | 24K tokens image+text; 8192 for generation |
| Architecture | VLM with Parallel Box Decoding (PBD) |
| Training data | 138M samples, 785M bounding boxes |
| License | NVIDIA non-commercial (research/academic only) |

---

## What it does

LocateAnything answers natural-language localization queries against images:

| Query type | Example | Output |
|-----------|---------|--------|
| Object detection | "Locate all cars" | Bounding boxes around each car |
| Phrase grounding | "The woman in the red hat" | Box around that specific person |
| Text/OCR localization | "Find the price tag" | Box around the text region |
| GUI grounding | "The submit button" | Box for automation agents |
| Point queries | "Where is the cat?" | Centre-point coordinate |

Coordinates are normalized to [0, 1000]:
```
<box><x1><y1><x2><y2></box>   # bounding box
<box><x><y></box>             # point
```

**Architecture:** Uses **Parallel Box Decoding (PBD)** — block-wise multi-token prediction for coordinates, much faster than autoregressive decoding. This is why it can handle dense detection (many boxes) efficiently.

---

## Benchmarks

| Task | LocateAnything-3B | Notes |
|------|------------------|-------|
| GUI grounding (mean F1) | 60.3 | Beats Qwen3-VL-30B-A3B |
| Dense detection (mean F1) | 39.9–58.7 | Varies by dataset |

Not a COCO-class detector — designed for open-vocabulary, instruction-driven localization rather than fixed category sets.

---

## Running locally

**Requirements:** CUDA GPU, Python, transformers==4.57.1.

```bash
pip install opencv-python-headless==4.11.0.86 \
            transformers==4.57.1 \
            numpy==1.25.0 Pillow==11.1.0 \
            peft torchvision decord==0.6.0 lmdb==1.7.5
# Install PyTorch separately for your CUDA version
```

**Quick usage:**

```python
from transformers import pipeline

pipe = pipeline(
    "image-text-to-text",
    model="nvidia/LocateAnything-3B",
    trust_remote_code=True,
)

messages = [{
    "role": "user",
    "content": [
        {"type": "image", "url": "https://example.com/photo.jpg"},
        {"type": "text", "text": "Locate all dogs in this image."},
    ],
}]

result = pipe(text=messages)
print(result)
# → [{'generated_text': '<box>312<455<589<701></box> <box>...'}]
```

**Generation modes** (pass as `generation_mode` kwarg):

| Mode | Speed | Quality |
|------|-------|---------|
| `hybrid` | Medium | Best (default) |
| `fast` | Fast | Good (MTP only) |
| `slow` | Slow | Highest (autoregressive) |

---

## Use cases

| Use case | Notes |
|----------|-------|
| Visual search / image retrieval | Find specific objects in large image sets |
| Computer-use agents | Locate UI elements for clicking (pairs with Holo) |
| Document / form parsing | Find fields in scanned documents |
| Robotics / pick-and-place | Locate objects for manipulation |
| Dataset annotation | Auto-annotate bounding boxes from descriptions |

!!! warning "Licence restriction"
    LocateAnything-3B is released under the **NVIDIA non-commercial licence** — academic and research use only. Commercial deployment requires a separate agreement with NVIDIA.

---

## Source & licence

- **Weights**: [huggingface.co/nvidia/LocateAnything-3B](https://huggingface.co/nvidia/LocateAnything-3B)
- **Licence**: NVIDIA non-commercial (research/academic only)
