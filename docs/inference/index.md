# Inference Runtimes

Local inference engines and servers.

| Tool | Install | API port |
|------|---------|----------|
| [Ollama](ollama.md) | `curl … \| sh` | 11434 |
| [llama.cpp](llama-cpp.md) | brew / build from source | 8080 |
| [LM Studio](lm-studio.md) | `curl … \| bash` | 1234 |

## Optimization

| Technique | What it does |
|-----------|-------------|
| [TurboQuant](turboquant.md) | 6× KV cache compression, no retraining — extends usable context and batch size |
