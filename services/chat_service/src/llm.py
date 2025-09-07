import requests
from config import model_settings


class LLM:
    def get_text_response(self, prompt: str) -> str:
        payload = {
            "model": model_settings.OLLAMA_MODEL,
            "prompt": prompt,
            "temperature": 0.7,
        }
        try:
            response = requests.post(
                model_settings.OLLAMA_URL, json=payload, timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"].strip()
        except Exception as e:
            print("Error calling Ollama:", e)
            return ""
