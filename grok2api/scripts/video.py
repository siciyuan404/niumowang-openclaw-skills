#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate videos using Grok Imagine Video.
Usage: python video.py "A cat jumping over a fence" [--output video.mp4]
"""

import sys
import json
import requests
import base64
import os


def generate_video(prompt: str, output_path: str = None, duration: int = 5) -> None:
    """Generate a video from text prompt."""
    BASE_URL = "http://localhost:8000"
    API_KEY = "123456"
    MODEL = "grok-imagine-1.0-video"

    url = f"{BASE_URL}/v1/videos/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "duration": duration  # Duration in seconds
    }

    try:
        print(f"Generating video for: \"{prompt}\"")
        print("(This may take a while...)")
        response = requests.post(url, headers=headers, json=payload, timeout=300)  # 5 min timeout
        response.raise_for_status()

        result = response.json()

        if 'data' in result and len(result['data']) > 0:
            video_data = result['data'][0]

            if 'url' in video_data:
                # Download video
                video_response = requests.get(video_data['url'], stream=True)
                video_response.raise_for_status()

                if output_path is None:
                    safe_prompt = "".join(c if c.isalnum() or c in " -_" else "_" for c in prompt)[:50]
                    output_path = f"{safe_prompt}.mp4"

                with open(output_path, 'wb') as f:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        f.write(chunk)

                file_size = os.path.getsize(output_path)
                print(f"✓ Video saved to: {output_path}")
                print(f"  Size: {file_size / (1024*1024):.2f} MB")
            else:
                print("Error: No video URL in response", file=sys.stderr)
                print(json.dumps(result, indent=2), file=sys.stderr)
                sys.exit(1)
        else:
            print("Error: No video data in response", file=sys.stderr)
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
        print("Usage: python video.py \"Your prompt\" [--output video.mp4] [--duration SECONDS]", file=sys.stderr)
        print("Example: python video.py \"A cat jumping over a fence\"", file=sys.stderr)
        print("Options:", file=sys.stderr)
        print("  --output FILE     Output filename (default: auto-generated)", file=sys.stderr)
        print("  --duration SEC    Video duration in seconds (default: 5)", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = None
    duration = 5

    # Parse optional arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--duration" and i + 1 < len(sys.argv):
            duration = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    generate_video(prompt, output_path, duration)


if __name__ == "__main__":
    main()
