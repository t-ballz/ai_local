# Miso One (TTS)

> Source: [github.com/MisoLabsAI/MisoTTS](https://github.com/MisoLabsAI/MisoTTS) · [HuggingFace MisoLabsAI](https://huggingface.co/MisoLabsAI)

## TL;DR

Miso Labs' open-weight **text-to-speech** model. 8B parameters, 110 ms latency (faster than average human speech reaction time), one-shot voice cloning from a 10-second sample. Fully open-source (weights + inference code). Requires a CUDA GPU — not GGUF-quantized, no CPU path. Currently a single model (no size variants).

---

## Model specs

| Property | Value |
|----------|-------|
| Parameters | 8B |
| Latency | ~110 ms first-audio |
| Voice cloning | One-shot from ~10 s reference audio |
| Multi-speaker | Yes |
| Streaming | Yes (real-time) |
| Format | PyTorch (bfloat16); no GGUF |
| License | Open-source (check repo for exact terms) |

---

## What it does

Miso One generates conversational speech with natural prosody, pacing, and emotional range. Key features:

- **One-shot voice cloning** — provide a short audio clip; the model conditions on speaker timbre without fine-tuning
- **Audio continuation** — condition on prior audio to keep voice and style consistent across turns
- **Real-time streaming** — 110 ms latency is below perceptible delay for interactive apps
- **Multi-speaker** — handles dialogue between different speakers in a single generation

---

## Running locally

**Requirements:** Python 3.10, CUDA GPU (GPU is required — 8B at bfloat16 is ~16 GB VRAM).

```bash
git clone https://github.com/MisoLabsAI/MisoTTS.git
cd MisoTTS
uv sync --python 3.10   # uses UV package manager
python run_misotts.py
```

!!! warning "GPU required"
    Miso One runs in bfloat16 — no 4-bit quantization available yet. You need a GPU with ~16 GB VRAM (RTX 3090, 4090, A4000, etc.). CPU inference is not practical.

---

## Use cases

| Use case | Notes |
|----------|-------|
| Voice cloning / dubbing | Clone any voice from a 10 s sample |
| Interactive AI assistants | Real-time, low-latency responses |
| Podcast / audiobook generation | Consistent multi-speaker dialogue |
| Localisation / voiceover | Replace reference voice with cloned target |

---

## Source & licence

- **Source**: [github.com/MisoLabsAI/MisoTTS](https://github.com/MisoLabsAI/MisoTTS)
- **Weights**: [huggingface.co/MisoLabsAI](https://huggingface.co/MisoLabsAI)
