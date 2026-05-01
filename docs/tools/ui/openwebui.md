# Open WebUI

> Source: [github.com/open-webui/open-webui](https://github.com/open-webui/open-webui) · [docs.openwebui.com](https://docs.openwebui.com)

## TL;DR

Self-hosted, offline-capable ChatGPT-style UI that connects to Ollama, any OpenAI-compatible backend, or runs its own bundled Ollama. Docker is the recommended deploy path. The first account created becomes admin.

---

## Install

=== "pip (Python 3.11+)"
    ```bash
    pip install open-webui
    open-webui serve
    # → http://localhost:8080
    ```

=== "Docker — bundled Ollama (GPU)"
    ```bash
    docker run -d -p 3000:8080 --gpus=all \
      -v ollama:/root/.ollama \
      -v open-webui:/app/backend/data \
      --name open-webui --restart always \
      ghcr.io/open-webui/open-webui:ollama
    ```

=== "Docker — bundled Ollama (CPU)"
    ```bash
    docker run -d -p 3000:8080 \
      -v ollama:/root/.ollama \
      -v open-webui:/app/backend/data \
      --name open-webui --restart always \
      ghcr.io/open-webui/open-webui:ollama
    ```

!!! warning "Always mount the data volume"
    `-v open-webui:/app/backend/data` persists your users, history, and settings. Omitting it means data loss on container restart.

---

## Connecting to a backend

### External Ollama on the same machine

```bash
docker run -d -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

`host.docker.internal` resolves to the host's `localhost`, so Ollama on `127.0.0.1:11434` is reachable without extra config.

### External Ollama on another machine (LAN)

```bash
docker run -d -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://192.168.1.50:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

### OpenAI-compatible backend (llama.cpp server, LM Studio, etc.)

Set `OPENAI_API_BASE_URL` to your backend's base URL:

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_BASE_URL=http://192.168.1.50:8080/v1 \
  -e OPENAI_API_KEY=none \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

### Cloud OpenAI API

```bash
docker run -d -p 3000:8080 \
  -e OPENAI_API_KEY=sk-... \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
```

---

## LAN / network hosting

To make the container reachable by other devices on your network:

```bash
# Option A: expose on all interfaces (port 3000 → container 8080)
docker run -d -p 0.0.0.0:3000:8080 ...
# Access from LAN: http://<host-ip>:3000

# Option B: host network mode (no NAT, container uses port 8080 directly)
docker run -d --network=host \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  -v open-webui:/app/backend/data \
  --name open-webui --restart always \
  ghcr.io/open-webui/open-webui:main
# Access from LAN: http://<host-ip>:8080
```

---

## Security

### First-run admin

The **first account registered** automatically becomes Administrator. Do this immediately after deploy before exposing the service.

### Secret key (required for persistent sessions)

Generate once and store it — users will be logged out whenever the container is recreated without it:

```bash
openssl rand -hex 32   # generate
```

```bash
docker run -d ... -e WEBUI_SECRET_KEY="<your-key>" ...
```

### Disable public signup

After creating your account(s), prevent new registrations:

| Env var | Value | Effect |
|---------|-------|--------|
| `ENABLE_SIGNUP` | `False` | Hides the sign-up form |
| `WEBUI_AUTH` | `False` | Disables login entirely (single-user, trusted network only) |

!!! warning "Auth mode is permanent"
    You cannot switch between `WEBUI_AUTH=False` (single-user) and multi-account mode after first run. Decide upfront.

### docker-compose example (production-ish)

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    ports:
      - "3000:8080"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - WEBUI_SECRET_KEY=<generate-with-openssl>
      - ENABLE_SIGNUP=False
    extra_hosts:
      - "host.docker.internal:host-gateway"
    volumes:
      - open-webui:/app/backend/data
    restart: unless-stopped

volumes:
  open-webui:
```

---

## Source code

[github.com/open-webui/open-webui](https://github.com/open-webui/open-webui) — MIT license
