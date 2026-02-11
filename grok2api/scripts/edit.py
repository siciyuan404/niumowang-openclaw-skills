#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edit images using Grok Imagine Edit.
Usage: python edit.py input.png "A cat wearing sunglasses" [--output output.png]
"""

import sys
import json
import requests
import base64
from PIL import Image
from io import BytesIO
import os


def encode_image_to_base64(image_path: str) -> str:
    """Encode an image file to base64."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def edit_image(input_path: str, prompt: str, output_path: str = None) -> None:
    """Edit an image with a text prompt."""
    # Validate input
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Service configuration
    BASE_URL = "http://localhost:8000"
    API_KEY = "123456"
    MODEL = "grok-imagine-1.0-edit"

    url = f"{BASE_URL}/v1/images/edits"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }

    try:
        print(f"Editing image: {input_path}")
        print(f"Prompt: \"{prompt}\"")

        # Prepare multipart form data
        with open(input_path, 'rb') as image_file:
            files = {
                'image': (os.path.basename(input_path), image_file, 'image/png')
            }
            data = {
                'model': MODEL,
                'prompt': prompt,
                'n': 1,
                'size': '1024x1024'
            }

            response = requests.post(url, headers=headers, files=files, data=data, timeout=60)
            response.raise_for_status()

        result = response.json()

        if 'data' in result and len(result['data']) > 0:
            image_data = result['data'][0]

            if 'url' in image_data:
                img_response = requests.get(image_data['url'])
                img = Image.open(BytesIO(img_response.content))
            elif 'b64_json' in image_data:
                img_bytes = base64.b64decode(image_data['b64_json'])
                img = Image.open(BytesIO(img_bytes))
            else:
                print("Error: Unknown image format", file=sys.stderr)
                sys.exit(1)

            if output_path is None:
                name, ext = os.path.splitext(input_path)
                output_path = f"{name}_edited{ext}"

            img.save(output_path)
            print(f"✓ Edited image saved to: {output_path}")
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
    if len(sys.argv) < 3:
        print("Usage: python edit.py input.png \"Your edit prompt\" [--output output.png]", file=sys.stderr)
        print("Example: python edit.png photo.png \"Add sunglasses to the person\"", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    prompt = sys.argv[2]
    output_path = None

    if len(sys.argv) >= 4 and sys.argv[3] == "--output" and len(sys.argv) >= 5:
        output_path = sys.argv[4]

    edit_image(input_path, prompt, output_path)


if __name__ == "__main__":
    main()
