# Porting Moebius 0.2B to Browser with WebGPU

> Source: [simonwillison.net](https://simonwillison.net/2026/Jun/22/porting-moebius/) · June 2026  
> Engineer: Simon Willison · Assisted by Claude Opus 4.8

## TL;DR

Simon Willison successfully ported the lightweight Moebius 0.2B image inpainting model to run entirely in the browser using WebGPU and ONNX Runtime Web. The conversion involved PyTorch → ONNX export, ONNX Runtime Web deployment on WebGPU backend, and CacheStorage-based model weight caching to eliminate repeated 1.3GB downloads. The completed demo runs on Chrome, Firefox, and Safari with no server-side GPU required.

---

## The problem

The Moebius model is compact (0.22B parameters) and fast, making it ideal for edge deployment. However, hosting it typically requires:
- Server-side infrastructure with GPU capability
- Network bandwidth for inference requests and responses
- Model serving overhead

A more user-friendly approach would distribute computation to the client: run the model directly in the user's browser, eliminating server costs and offering instant, private inference.

---

## Conversion pipeline

### PyTorch to ONNX

The first step was exporting the pretrained Moebius model from PyTorch to ONNX format:

- **Opset version**: 18 (ensures broad operator compatibility across runtimes)
- **Dynamic axes**: Configured for variable batch sizes and sequence dimensions
- **Named tensors**: Explicitly labeled input/output nodes for clarity

This conversion preserves the model's behavior while creating a runtime-agnostic representation.

### ONNX Runtime Web with WebGPU backend

Rather than using JavaScript transformers libraries, the implementation adopted **ONNX Runtime Web** running on a **WebGPU backend**. This approach provided:

- **Lower-level control**: Direct GPU compute without JavaScript abstraction layers
- **Performance**: Efficient tensor operations via native WebGPU compute shaders
- **Stability**: ONNX Runtime's C++ core compiled to WebAssembly with proven GPU interop

The WebGPU backend handles all tensor computations on the GPU, while JavaScript orchestrates model loading and input/output handling.

---

## Browser caching: CacheStorage API

A critical bottleneck emerged: the ONNX model weights total ~1.3GB, and downloading them on every page reload was impractical. The solution leveraged the **CacheStorage API**:

```javascript
const cache = await caches.open("transformers-cache");
// Store model weights on first load
await cache.put(modelUrl, response);
// Retrieve from cache on subsequent loads
const cached = await cache.match(modelUrl);
```

This enables persistent browser caching across page reloads, turning the first load into a one-time cost while subsequent sessions start instantly.

---

## Browser compatibility

WebGPU support has reached critical mass across major browsers:

| Browser | Support |
|---------|---------|
| Chrome | ✓ |
| Firefox | ✓ |
| Safari | ✓ |

All three browsers now expose the WebGPU API, allowing the application to run universally without fallbacks.

---

## Key learnings

The project demonstrated that Claude Opus 4.8 can autonomously handle complex, multi-domain tasks without manual code writing:

- **Model format conversion**: PyTorch → ONNX export with proper tensor configuration
- **Runtime selection**: Evaluating ONNX Runtime Web over lighter-weight alternatives for performance
- **WebGPU integration**: Writing compute-shader-aware code for efficient GPU operations
- **Web application development**: Building a complete UI with model caching, progress indicators, and error handling
- **Hugging Face publishing**: Uploading the converted model to HuggingFace for community access

This capability ("vibe coding") suggests that future AI-assisted development may focus on human intent and design rather than implementation details.

---

## Resources

- **Live demo**: [simonw.github.io/moebius-web/](https://simonw.github.io/moebius-web/)
- **ONNX model weights**: [huggingface.co/simonw/Moebius-ONNX](https://huggingface.co/simonw/Moebius-ONNX)
- **Original Moebius paper**: [Moebius: Lightweight Image Inpainting Framework](moebius-image-inpainting.md)
- **Technology**: ONNX Runtime Web, WebGPU, CacheStorage API, JavaScript/React

---

## Related work

- [Moebius: Lightweight Image Inpainting Framework](moebius-image-inpainting.md) — the original 0.2B model architecture and distillation approach
- Browser-based ML inference via WebGPU and WASM (emerging standard for client-side model execution)
- Model compression and quantization as enablers for browser deployment
