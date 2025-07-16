import os
import requests
from dotenv import load_dotenv

load_dotenv()

LANGUAGE_CODES = {
    "english": "en", "french": "fr", "telugu": "te", "hindi": "hi",
    "spanish": "es", "german": "de", "chinese": "zh", "japanese": "ja",
    "italian": "it", "korean": "ko", "arabic": "ar", "russian": "ru",
    "tamil": "ta", "bengali": "bn", "urdu": "ur"
}

def translate_text(text, target_lang="en"):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("Missing OPENROUTER_API_KEY in environment variables.")

    lang_code = LANGUAGE_CODES.get(target_lang.lower(), target_lang)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",  # REQUIRED
        "HTTP-Referer": "http://localhost",  # REQUIRED
        "X-Title": "Voice of the City"
    }

    prompt = f"Translate this to {lang_code}:\n\n{text}"

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"Translation failed: {response.status_code} - {response.text}")
