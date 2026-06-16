# Whisper Large V3 Turbo

> Source: [HuggingFace](https://huggingface.co/openai/whisper-large-v3-turbo) · OpenAI · October 2024  
> License: MIT

## TL;DR

A distilled variant of Whisper Large V3 with the decoder pruned from 32 layers to 4, cutting parameters from 1.55B to 809M and delivering **4–8× faster transcription** with minimal accuracy loss. Supports 99 languages. Not trained for translation — transcription only. Runs comfortably on consumer hardware: int8-quantized fits in 1.5 GB VRAM.

---

## Architecture

| | Large V3 | Large V3 Turbo |
|--|---------|----------------|
| Parameters | 1,550M | **809M** |
| Decoder layers | 32 | **4** |
| Encoder | unchanged | unchanged |
| Context (audio) | 30s chunks | 30s chunks |
| Languages | 99 | 99 |
| Translation task | Yes | **No** |

The encoder is identical to Large V3; only the decoder was pruned. The tradeoff: generation is much faster (fewer autoregressive steps) with only a small WER increase.

---

## Benchmarks

| Benchmark | WER |
|-----------|-----|
| Mean WER (open-asr-leaderboard) | 7.83 |
| AMI (meetings) | 16.13 |
| Real-time factor (RTFX) | 200× |

Speed vs Large V3: **4–8× faster** depending on hardware and batch size. On YouTube-commons: 13.40% WER (Turbo) vs 13.20% (V3) at 2.3× the speed — essentially a free lunch for most use cases.

---

## Local inference options

| Backend | Best for | VRAM (int8) |
|---------|----------|-------------|
| **faster-whisper** | GPU throughput in Python | ~1.5 GB |
| **whisper.cpp** | CPU / edge / portable GGUF | CPU-only possible |
| **mlx-whisper** | Apple Silicon | unified memory |
| **transformers** | HuggingFace ecosystem | ~1.6 GB (float16) |

### faster-whisper (CTranslate2)

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3-turbo", device="cuda", compute_type="int8")
segments, info = model.transcribe("audio.mp3")
for segment in segments:
    print(f"[{segment.start:.1f}s] {segment.text}")
```

### transformers pipeline

```python
from transformers import pipeline

pipe = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3-turbo",
    device="cuda",
)
result = pipe("audio.mp3")
print(result["text"])
```

For audio longer than 30 seconds, use `chunk_length_s=30` to enable chunked long-form processing.

### whisper.cpp (GGUF)

GGUF-converted models are available on HuggingFace (search `whisper-large-v3-turbo gguf`). Load with whisper.cpp as normal.

---

## Speed optimisations

- **`torch.compile`**: 4.5× speedup on top of the base model speed
- **Flash Attention 2**: pass `attn_implementation="flash_attention_2"` to `from_pretrained`
- **int8 quantization**: halves memory vs float16 with negligible quality drop
- **Batched inference**: faster-whisper supports `beam_size` and batch processing for high-throughput pipelines

---

## Limitations

- **No translation**: unlike other Whisper variants, Turbo was not fine-tuned for speech-to-text translation — only transcription
- **30s encoder window**: long audio must be chunked; timestamps can drift on very long files
- **Accuracy gap**: small but real WER increase vs Large V3, more noticeable on heavily accented or noisy audio

---

## Source

- **HuggingFace**: [openai/whisper-large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo)
- **faster-whisper**: [SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
- **whisper.cpp**: [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp)
