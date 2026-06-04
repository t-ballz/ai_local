# Ideogram 4.0

> Source: [ideogram.ai/blog/ideogram-4.0](https://ideogram.ai/blog/ideogram-4.0/) · [github.com/ideogram-oss/ideogram4](https://github.com/ideogram-oss/ideogram4) · [HuggingFace ideogram-ai](https://huggingface.co/ideogram-ai)

## TL;DR

Ideogram's open-weight **text-to-image** diffusion model (June 3, 2026). 9.3B parameters, native **2K resolution** output, and by far the best text-rendering quality among open-weight image generators. Runs on a single 24 GB GPU (NF4 quantization). ComfyUI support from day one. Gated HuggingFace download (accept licence, then free). Ranked #1 on DesignArena among open-weight models.

---

## Model specs

| Property | Value |
|----------|-------|
| Parameters | 9.3B |
| Architecture | DiT (Diffusion Transformer), 34 layers |
| Native output resolution | Up to 2048 × 2048 (2K) |
| Min / max side length | 256–2048 px (any multiple of 16) |
| Prompt length | Up to 4K tokens |
| Quantizations | NF4 (single 24 GB GPU), FP8 (broader GPU support) |
| License | Gated — see [github.com/ideogram-oss/ideogram4](https://github.com/ideogram-oss/ideogram4) |

---

## Key features

**Text rendering** — the main differentiator. Ideogram 4.0 is the first open-weight model to reliably render legible, correctly spelled text in images — useful for posters, logos, UI mockups, and any design work involving typography.

**Layout control via bounding boxes** — specify where elements should appear using normalized coordinates [y_min, x_min, y_max, x_max] in 0–1000 space.

**Transparent backgrounds** — natively generate PNG assets with alpha channel for compositing.

**Colour conditioning** — pass a hex colour palette in the style description to steer the output palette.

---

## Running locally

**Step 1: Get access**

```bash
# Weights are gated on HuggingFace — accept licence first:
# huggingface.co/ideogram-ai/ideogram-4-nf4  (24 GB GPU)
# huggingface.co/ideogram-ai/ideogram-4-fp8  (FP8, broader support)

export HF_TOKEN="hf_..."
```

**Step 2: Clone and install**

```bash
git clone https://github.com/ideogram-oss/ideogram4
cd ideogram4
pip install -r requirements.txt
```

**Step 3: Generate an image**

```python
from ideogram4 import Ideogram4Pipeline

pipe = Ideogram4Pipeline.from_pretrained(
    "ideogram-ai/ideogram-4-nf4",
    token=os.environ["HF_TOKEN"],
)

image = pipe(
    prompt="A retro diner sign reading 'Joe's Place' with neon lettering on a black background",
    width=1024,
    height=1024,
).images[0]

image.save("output.png")
```

**ComfyUI:** Install the Ideogram 4.0 custom node from the ComfyUI Manager — day-0 support included.

---

## Layout / text control

Pass structured JSON instead of plain text for precise placement:

```json
{
  "prompt": "Poster design",
  "elements": [
    {
      "text": "SALE",
      "bbox": [50, 100, 300, 400],
      "style": "bold sans-serif, red"
    },
    {
      "text": "50% off everything",
      "bbox": [50, 420, 500, 550]
    }
  ]
}
```

Bounding box format: `[y_min, x_min, y_max, x_max]` normalized to [0, 1000].

---

## Quality comparison

| Model | Text rendering | Overall quality | Open-weight |
|-------|--------------|-----------------|-------------|
| Ideogram 4.0 | ★★★★★ | ★★★★☆ (#1 open) | Yes (gated) |
| Flux.1 | ★★★★☆ | ★★★★☆ | Yes |
| SDXL | ★★☆☆☆ | ★★★☆☆ | Yes |
| GPT-Image-2 | ★★★★★ | ★★★★★ | No (API) |

Ideogram 4.0 ranks below closed models (GPT-Image-2, Luma Uni-1.1) overall, but leads all open-weight models and is the clear choice when readable text in the image is a hard requirement.

---

## Use cases

| Use case | Notes |
|----------|-------|
| Graphic design / posters | Native 2K, layout + text control |
| Logo / brand assets | Transparent background support |
| UI mockups | Text elements render correctly |
| Marketing materials | Colour palette conditioning |
| Dataset generation | Better at consistent typography than alternatives |

---

## Source & licence

- **Code**: [github.com/ideogram-oss/ideogram4](https://github.com/ideogram-oss/ideogram4)
- **Weights (NF4)**: [huggingface.co/ideogram-ai/ideogram-4-nf4](https://huggingface.co/ideogram-ai/ideogram-4-nf4)
- **Weights (FP8)**: [huggingface.co/ideogram-ai/ideogram-4-fp8](https://huggingface.co/ideogram-ai/ideogram-4-fp8)
- **Licence**: Gated — accept on HuggingFace before downloading
