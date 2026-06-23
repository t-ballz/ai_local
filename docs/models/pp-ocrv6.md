# PP-OCRv6

> Source: [HuggingFace](https://huggingface.co/collections/PaddlePaddle/pp-ocrv6) · PaddlePaddle · 2024  
> License: Apache 2.0

## TL;DR

PaddlePaddle's open-source OCR system with three model sizes (1.5M–34.5M parameters) supporting 50 languages. The medium variant achieves 86.2% detection and 83.2% recognition accuracy, representing **+4.6%** and **+5.1%** improvements over PPv5. Runs efficiently on CPU/GPU via PaddleOCR, PyTorch/Transformers, or ONNX Runtime.

---

## Overview

PP-OCRv6 is an ultra-lightweight, multilingual optical character recognition system designed for practical deployment across mobile, cloud, and edge devices. The system separates text detection and recognition into two cascading models, allowing fine-grained control over speed/accuracy tradeoffs.

**Architecture:**
- **Detector**: RepLKFPN (large-kernel feature pyramid network) for text region localization
- **Recognizer**: EncoderWithLightSVTR for character-level recognition
- **Backbone**: PPLCNetV4 for efficient feature extraction

---

## Models & Sizes

Three variants balance speed and accuracy:

| Model | Parameters | Detection Hmean | Recognition Accuracy | Use case |
|-------|-----------|-----------------|----------------------|----------|
| **PP-OCRv6_tiny** | 1.5M | 80.6% | 73.5% | Edge/mobile, real-time inference |
| **PP-OCRv6_small** | 7.7M | 84.1% | 81.3% | Balanced speed/accuracy |
| **PP-OCRv6_medium** | 34.5M | **86.2%** | **83.2%** | High accuracy, server-side |

All weights are available on HuggingFace with downloadable `.pdmodel` and `.pdiparams` files.

---

## Languages

The small and medium tiers support **50 languages**:

- **CJK**: Simplified Chinese, Traditional Chinese, Japanese
- **Latin scripts**: English and 46 additional Latin-based languages (German, French, Spanish, Russian, Arabic, etc.)
- **Tiny**: Focuses on Chinese and English only

Full language list: [PP-OCRv6 Collection on HuggingFace](https://huggingface.co/collections/PaddlePaddle/pp-ocrv6)

---

## Benchmarks

Compared to PP-OCRv5 (server variant):

| Metric | Improvement |
|--------|-------------|
| Text detection (Hmean) | **+4.6%** |
| Character recognition | **+5.1%** |

Performance on standard benchmarks:

- **Real-time inference**: Medium variant at ~100 FPS on GPU (batch=1)
- **Mobile deployment**: Tiny variant fits in <10 MB disk; inference under 100 ms on modern mobile CPUs
- **Multilingual robustness**: Achieves >80% accuracy across diverse language families

---

## Usage & Backends

### PaddleOCR (default backend)

```python
from paddleocr import PaddleOCR

# Automatic model selection (defaults to medium)
ocr = PaddleOCR(use_doc_orientation_classify=False)
result = ocr.ocr("image.jpg", cls=False)

for line in result:
    for word_info in line:
        print(f"{word_info[1][0]:.2f}% - {word_info[0]}")  # confidence & text
```

### PyTorch / Transformers backend

```python
# Use Transformers for integration with HuggingFace ecosystem
ocr = PaddleOCR(engine="transformers", lang="en")
result = ocr.ocr("image.jpg")
```

### ONNX Runtime (fastest CPU inference)

```python
# Cross-platform, hardware-optimized inference
ocr = PaddleOCR(engine="onnxruntime")
result = ocr.ocr("image.jpg")
```

### Installation

```bash
pip install paddleocr

# Optional: GPU support
pip install paddlepaddle-gpu
```

---

## Inference on Consumer Hardware

| Setup | Memory | Speed (Medium) |
|-------|--------|----------------|
| CPU (8-core) | ~200 MB | ~50 ms/image |
| GPU (RTX 3080) | ~500 MB | ~10 ms/image |
| Mobile (ARM64) | ~50 MB (tiny) | ~200 ms/image (tiny) |

---

## Source

- **HuggingFace Collection**: [PaddlePaddle/pp-ocrv6](https://huggingface.co/collections/PaddlePaddle/pp-ocrv6)
- **Online Demo**: [PP-OCRv6 Hugging Face Space](https://huggingface.co/spaces/PaddlePaddle/PP-OCRv6)
- **PaddleOCR Docs**: [Official documentation](https://paddleocr.readthedocs.io/)
- **GitHub**: [PaddleOCR Repository](https://github.com/PaddlePaddle/PaddleOCR)
