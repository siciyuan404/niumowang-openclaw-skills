---
name: grok2api
description: Control and interact with local grok2api service (port 8000, API key: 123456). Use for chat completion requests, model listing, and testing Grok models (grok-3, grok-4, grok-4.1 series, and image/video generation models). Trigger when user asks to use Grok, test the API, or interact with the local service.
---

# Grok2api

本地 grok2api 服务的控制接口。

## Service Configuration

- **Base URL:** `http://localhost:8000`
- **API Key:** `123456`
- **OpenAI-Compatible:** Yes (uses `/v1/` endpoints)

## Available Models

**Chat Models:**
- `grok-3` / `grok-3-mini` / `grok-3-thinking`
- `grok-4` / `grok-4-mini` / `grok-4-thinking` / `grok-4-heavy`
- `grok-4.1-mini` / `grok-4.1-fast` / `grok-4.1-expert` / `grok-4.1-thinking`

**Image/Video Models:**
- `grok-imagine-1.0` (image generation)
- `grok-imagine-1.0-edit` (image editing)
- `grok-imagine-1.0-video` (video generation)

## Quick Start

### List Available Models

```bash
curl.exe -s http://localhost:8000/v1/models -H "Authorization: Bearer 123456"
```

### Chat Completion (Non-Streaming)

```bash
curl.exe -s http://localhost:8000/v1/chat/completions `
  -H "Authorization: Bearer 123456" `
  -H "Content-Type: application/json" `
  --data-binary "@C:\path\to\request.json"
```

JSON payload example:
```json
{
  "model": "grok-3",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": false
}
```

### Chat Completion (Streaming)

Streaming is enabled by default. To receive streaming responses, omit `"stream": false` or set `"stream": true`.

## Using the Scripts

The `scripts/` directory contains helper utilities for common operations:

- `chat.py` - Send chat completions with streaming support
- `list_models.py` - List all available models

Run scripts from workspace root:
```bash
python scripts/grok2api/chat.py "Your message here"
python scripts/grok2api/chat.py "Your message" --model grok-4
python scripts/grok2api/list_models.py
```

## Troubleshooting

**Connection refused:** Ensure grok2api is running on port 8000.

**Invalid API key:** The service expects `123456`.

**PowerShell curl issues:** Use `curl.exe` instead of `curl` to avoid PowerShell alias conflicts.
