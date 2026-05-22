import os
import json
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # set locally
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def call_openai_daily(prompt_text: str, json_schema: dict, model: str) -> tuple[str, dict]:
    """
    Calls OpenAI and returns:
      - raw response text (assistant content)
      - parsed JSON dict
    Raises exceptions on failures.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY env var not set")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return only JSON that matches the schema."},
            {"role": "user", "content": prompt_text}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "daily_analysis_v1",
                "strict": True,
                "schema": json_schema
            }
        }
    }

    resp = requests.post(OPENAI_URL, headers=headers, json=body, timeout=60)
    resp.raise_for_status()

    data = resp.json()
    raw = data["choices"][0]["message"]["content"]
    parsed = json.loads(raw)
    return raw, parsed