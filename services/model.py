import subprocess
import requests

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