---
name: grok2api
description: Control and interact with local grok2api service (port 8000, API key: 123456). Use for chat completion, information retrieval with web search, image generation/editing, and video generation. Supports Grok models (grok-3, grok-4, grok-4.1 series) and Grok Imagine models (image/video). Trigger when user asks to use Grok, search for information, generate media, or interact with the local service.
---

# Grok2api

本地 grok2api 服务的完整控制接口。支持聊天、资讯查询、图片生成/编辑、视频生成。

## Service Configuration

- **Base URL:** `http://localhost:8000`
- **API Key:** `123456`
- **OpenAI-Compatible:** Yes (uses `/v1/` endpoints)

## Available Models

### Chat Models
- `grok-3` / `grok-3-mini` / `grok-3-thinking`
- `grok-4` / `grok-4-mini` / `grok-4-thinking` / `grok-4-heavy`
- `grok-4.1-mini` / `grok-4.1-fast` / `grok-4.1-expert` / `grok-4.1-thinking`

### Image/Video Models
- `grok-imagine-1.0` - 文生图
- `grok-imagine-1.0-edit` - 图片编辑
- `grok-imagine-1.0-video` - 文生视频

## Quick Start

### 资讯查询 (Web Search)

```bash
# 使用 grok-4.1-fast 快速查询资讯
python scripts/ask.py "今天的科技新闻有什么?"
python scripts/ask.py "最新的AI进展" --model grok-4.1-expert
```

### 图片生成

```bash
# 生成图片
python scripts/imagine.py "一只戴墨镜的猫"
python scripts/imagine.py "赛博朋克风格的上海" --output cyberpunk.png
```

### 图片编辑

```bash
# 编辑现有图片
python scripts/edit.png photo.png "给人物戴上墨镜" --output edited.png
python scripts/edit.png image.png "把背景改成海滩"
```

### 视频生成

```bash
# 生成短视频
python scripts/video.py "一只猫跳过栅栏"
python scripts/video.py "日落时分的海滩" --output sunset.mp4 --duration 10
```

### 聊天对话

```bash
# 普通聊天
python scripts/chat.py "你好，介绍一下你自己"
python scripts/chat.py "写一首关于春天的诗" --model grok-4
```

### 列出所有模型

```bash
python scripts/list_models.py
```

## Script Reference

### ask.py - 资讯查询
专门用于查询最新资讯和实时信息。Grok 具有联网搜索能力。

**用法:** `python ask.py "问题" [--model MODEL]`

**默认模型:** `grok-4.1-fast` (快速且知识丰富)

**示例:**
- 查新闻: `python ask.py "今天有什么重要新闻?"`
- 查事实: `python ask.py "GPT-5发布了吗?"`
- 查行情: `python ask.py "最新的AI股票走势"`

### imagine.py - 图片生成
根据文本描述生成图片。

**用法:** `python imagine.py "提示词" [--output 文件名.png]`

**默认格式:** PNG, 1024x1024

**示例:**
- `python imagine.py "一只在月球上的宇航员"`
- `python imagine.py "梵高风格的星空" --output starry.png`

### edit.py - 图片编辑
基于文本提示编辑现有图片。

**用法:** `python edit.png 输入文件.png "编辑提示" [--output 输出文件.png]`

**示例:**
- `python edit.png photo.png "把天空改成紫色"`
- `python edit.png portrait.png "添加眼镜" --output with_glasses.png`

### video.py - 视频生成
根据文本描述生成短视频。

**用法:** `python video.py "提示词" [--output 文件名.mp4] [--duration 秒数]`

**默认时长:** 5秒

**示例:**
- `python video.py "瀑布流淌的慢动作"`
- `python video.py "城市延时摄影" --output city.mp4 --duration 10`

### chat.py - 聊天对话
通用聊天和对话。

**用法:** `python chat.py "消息" [--model MODEL]`

**默认模型:** `grok-3`

### list_models.py - 模型列表
显示所有可用模型，按类型分组。

**用法:** `python list_models.py`

## Tips

- **资讯查询** 优先使用 `grok-4.1-fast`，速度快且知识新
- **复杂推理** 使用 `grok-4-thinking` 或 `grok-4.1-thinking`
- **创作任务** 使用 `grok-4-expert` 或 `grok-4.1-expert`
- **图片编辑** 需要提供原始图片路径
- **视频生成** 可能需要较长时间（1-5分钟）

## Troubleshooting

**Connection refused:** 确保 grok2api 在端口 8000 上运行

**Invalid API key:** 服务需要 `123456`

**PowerShell curl 问题:** 使用 `curl.exe` 而不是 `curl`

**图片/视频生成失败:** 检查网络连接，生成媒体需要与 xAI 服务器通信
