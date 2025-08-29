"""
Generate a photoreal sepia workplace background using the Hugging Face Inference API.

Usage:
  1. Set an environment variable named HUGGINGFACE_API_TOKEN with your HF token.
     In PowerShell:
       $Env:HUGGINGFACE_API_TOKEN = '<your-token>'

  2. Run this script with the project venv python:
       C:/Users/labadmin/Desktop/AISWE/AG-AISOFTDEV/venv/Scripts/python.exe scripts/generate_photoreal_background.py

The script will request a photoreal image (1920x1080) and save it as
`background_photoreal.png` in the project root. If you have no token, the
script will print instructions but will not attempt a request.

Notes:
 - This uses the Hugging Face Inference API endpoint. Usage may consume
   inference credits on your account.
 - If you'd like me to run this for you, provide a token or allow me to run
   an alternative generation pathway.
"""
import os
import sys
import base64
import json
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("This script requires the 'requests' package. Install with: pip install requests")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / 'background_photoreal.png'

HF_TOKEN = (
    os.environ.get('HUGGINGFACE_API_TOKEN')
    or os.environ.get('HF_API_TOKEN')
    or os.environ.get('HUGGINGFACE_API_KEY')
    or os.environ.get('HF_API_KEY')
)
if not HF_TOKEN:
    # Try to read a .env file in the project root for common keys
    env_path = ROOT / '.env'
    if env_path.exists():
        try:
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # simple KEY=VALUE or KEY="VALUE"
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip().strip('"').strip("'")
                    v = v.strip().strip('"').strip("'")
                    if k.upper() in ('HUGGINGFACE_API_TOKEN', 'HF_API_TOKEN', 'HUGGINGFACE_API_KEY', 'HF_API_KEY', 'HUGGINGFACE_API'):
                        HF_TOKEN = v
                        break
        except Exception:
            pass
if not HF_TOKEN:
    print("No Hugging Face token found in HUGGINGFACE_API_TOKEN or HF_API_TOKEN environment variables.")
    print("If you want to generate a photoreal image, set the env var and re-run the script.")
    print("Example (PowerShell): $Env:HUGGINGFACE_API_TOKEN = '<token>'")
    sys.exit(0)

# Choose a reasonably capable model name that supports text-to-image via HF inference.
# You can change this to another model you prefer (for example: 'runwayml/stable-diffusion-v1-5').
# Models to try in order. Some models may return 404 if unavailable for inference or if you
# don't have access; the script will attempt each until one succeeds.
MODELS = [
    # Try current stable-diffusion XL and base variants first
    'stabilityai/stable-diffusion-xl-base-1-0',
    'stabilityai/stable-diffusion-2',
    'stabilityai/stable-diffusion-2-1',
    'runwayml/stable-diffusion-v1-5',
    'stabilityai/stable-diffusion-xl-beta-v2-2',
    # Last-resort tiny test model for accounts without access to the above
    'hf-internal-testing/tiny-stable-diffusion'
]

PROMPT = (
    "photorealistic workplace scene, action moment but workplace-appropriate, subtle anime influence "
    "(soft facial features), a person at a desk with monitor and papers, dynamic yet calm composition, "
    "soft natural window light, high detail, cinematic depth of field, sepia tone wash, desaturated highlights, "
    "warm beige and brown palette, light overall so foreground text will remain readable, 16:9 aspect ratio"
)

payload = {
    "inputs": PROMPT,
    "options": {"wait_for_model": True},
    "parameters": {
        "width": 1920,
        "height": 1080,
        "num_inference_steps": 28,
        "guidance_scale": 7.5
    }
}

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Accept": "application/json"
}

saved = False
for MODEL in MODELS:
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    print(f"Requesting image from model {MODEL}... (this may take 10-60s)")
    try:
        resp = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
    except Exception as e:
        print(f"Request to {MODEL} failed with exception: {e}")
        continue

    if resp.status_code == 200:
        content_type = resp.headers.get('content-type', '')
        data = resp.content
        if 'application/json' in content_type:
            j = resp.json()
            b64 = None
            if isinstance(j, dict) and 'image_base64' in j:
                b64 = j['image_base64']
            elif isinstance(j, dict) and 'images' in j and isinstance(j['images'], list):
                b64 = j['images'][0]
            if not b64:
                print('Unexpected JSON response from model. Here is a snippet:')
                print(json.dumps(j)[:2000])
                continue
            data = base64.b64decode(b64)

        OUT_PATH.write_bytes(data)
        print(f"Saved photoreal background to {OUT_PATH} (model: {MODEL})")
        saved = True
        break

    # Handle common non-success codes with helpful messages and fallbacks
    if resp.status_code == 404:
        print(f"Model {MODEL} not found (404). Trying next fallback model.")
        continue
    if resp.status_code == 403:
        print(f"Access to model {MODEL} forbidden (403). You may need to accept the model license or change model.")
        continue
    if resp.status_code == 503:
        print(f"Model {MODEL} currently unavailable (503). Trying next fallback model.")
        continue

    # Other codes - print a short response and try next
    print(f"Request to model {MODEL} returned status {resp.status_code}. Response snippet:")
    try:
        print(resp.json())
    except Exception:
        print(resp.text[:1000])

if not saved:
    print("All model attempts failed. See messages above. You can try a different model name or ensure your token has access.")