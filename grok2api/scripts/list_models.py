#!/usr/bin/env python3
"""
List all available models from grok2api service.
"""

import requests
import json

# Service configuration
BASE_URL = "http://localhost:8000"
API_KEY = "123456"


def list_models():
    """Fetch and display available models."""
    url = f"{BASE_URL}/v1/models"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        models = data.get('data', [])

        print(f"\nAvailable models ({len(models)}):\n")

        # Group by type
        chat_models = []
        image_models = []
        thinking_models = []

        for model in models:
            model_id = model.get('id', '')
            if 'imagine' in model_id:
                image_models.append(model_id)
            elif 'thinking' in model_id:
                thinking_models.append(model_id)
            else:
                chat_models.append(model_id)

        if chat_models:
            print("Chat Models:")
            for m in sorted(chat_models):
                print(f"  - {m}")

        if thinking_models:
            print("\nThinking Models:")
            for m in sorted(thinking_models):
                print(f"  - {m}")

        if image_models:
            print("\nImage/Video Models:")
            for m in sorted(image_models):
                print(f"  - {m}")

        print()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(list_models())
