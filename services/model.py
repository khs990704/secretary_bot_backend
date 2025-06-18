import requests
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL, MODEL_NAME

def call_model(prompt: str) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    res = requests.post(OPENROUTER_API_URL, headers=headers, json=body)
    return res.json()