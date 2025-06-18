import subprocess
import requests
# import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(message: str) -> str:
    payload = {
        "model": "openchat",
        "prompt": message,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=100)
        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()

    except Exception as e:
        return f"Error: {str(e)}"

# def stream_response(message: str) -> str:
#     payload = {
#         "model": "openchat",
#         "prompt": message,
#         "stream": True
#     }
#
#     response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=100)
#     buffer = ""
#
#     for line in response.iter_lines():
#         if line:
#             data = json.loads(line.decode("utf-8"))
#             buffer += data.get("response", "")
#             while len(buffer) >= 3:
#                 yield buffer[:3]
#                 buffer = buffer[3:]
#
#     if buffer:
#         yield buffer
#
#     return full_text.strip()