#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate images using Grok Imagine.
Usage: python imagine.py "A cat wearing sunglasses" [--output filename.png]
"""

import sys
import json
import requests
import base64
from PIL import Image
from io import BytesIO
import os
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Service configuration
BASE_URL = "http://localhost:8000"
API_KEY = "123456"
MODEL = "grok-imagine-1.0"


def generate_image(prompt: str, output_path: str = None) -> None:
    """Generate an image from text prompt."""
    url = f"{BASE_URL}/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    try:
        print(f"Generating image for: \"{prompt}\"")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()

        # Handle response format (may vary based on actual API)
        if 'data' in result and len(result['data']) > 0:
            image_data = result['data'][0]

            # Check for error response
            if 'url' in image_data and image_data['url'] == 'error':
                print("Error: Image generation failed. The grok2api service may not have image API configured.", file=sys.stderr)
                print("Please check your grok2api configuration or xAI API setup.", file=sys.stderr)
                sys.exit(1)

            # Check for URL or base64
            if 'url' in image_data:
                # Download from URL
                img_response = requests.get(image_data['url'])
                img = Image.open(BytesIO(img_response.content))
            elif 'b64_json' in image_data:
                # Decode base64
                img_bytes = base64.b64decode(image_data['b64_json'])
                img = Image.open(BytesIO(img_bytes))
            else:
                print("Error: Unknown image format in response", file=sys.stderr)
                sys.exit(1)

            # Save image
            if output_path is None:
                # Generate filename from prompt
                safe_prompt = "".join(c if c.isalnum() or c in " -_" else "_" for c in prompt)[:50]
                output_path = f"{safe_prompt}.png"

            img.save(output_path)
            print(f"✓ Image saved to: {output_path}")
            print(f"  Size: {img.size[0]}x{img.size[1]}")
        else:
            print("Error: No image data in response", file=sys.stderr)
            print(json.dumps(result, indent=2), file=sys.stderr)
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Usage: python imagine.py \"Your prompt\" [--output filename.png]", file=sys.stderr)
        print("Example: python imagine.py \"A cat wearing sunglasses\"", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = None

    if len(sys.argv) >= 3 and sys.argv[2] == "--output" and len(sys.argv) >= 4:
        output_path = sys.argv[3]

    generate_image(prompt, output_path)


if __name__ == "__main__":
    main()
