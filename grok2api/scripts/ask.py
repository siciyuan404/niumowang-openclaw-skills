#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ask Grok for information with web search capabilities.
Usage: python ask.py "Your question" [--model MODEL_NAME]
"""

import sys
import json
import requests
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Service configuration
BASE_URL = "http://localhost:8000"
API_KEY = "123456"
DEFAULT_MODEL = "grok-4.1-fast"  # Fast and knowledgeable


def ask(message: str, model: str = DEFAULT_MODEL) -> None:
    """Send a question to Grok with streaming."""
    url = f"{BASE_URL}/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # System prompt for information retrieval
    system_prompt = (
        "You are Grok, an AI with access to real-time information. "
        "When asked about current events, facts, or topics requiring up-to-date knowledge, "
        "search for and provide accurate, current information. Be concise but thorough."
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "stream": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)
        response.raise_for_status()

        print(f"\n[{model}] ", end="", flush=True)

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        print()
                        break
                    try:
                        data = json.loads(data_str)
                        delta = data.get('choices', [{}])[0].get('delta', {})
                        content = delta.get('content', '')
                        if content:
                            print(content, end="", flush=True)
                    except json.JSONDecodeError:
                        pass

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python ask.py \"Your question\" [--model MODEL_NAME]", file=sys.stderr)
        print(f"Default model: {DEFAULT_MODEL}", file=sys.stderr)
        sys.exit(1)

    message = sys.argv[1]
    model = DEFAULT_MODEL

    if len(sys.argv) >= 3 and sys.argv[2] == "--model" and len(sys.argv) >= 4:
        model = sys.argv[3]

    ask(message, model)


if __name__ == "__main__":
    main()
