import os
import requests

LANGUAGE_CODES = {
    "english": "en",
    "hindi": "hi",
    "telugu": "te",
    "tamil": "ta",
    "bengali": "bn",
    "marathi": "mr",
    "gujarati": "gu",
    "punjabi": "pa",
    "urdu": "ur",
    "kannada": "kn",
    "malayalam": "ml",
    "nepali": "ne",
    "french": "fr",
    "german": "de",
    "spanish": "es",
    "italian": "it",
    "chinese": "zh",
    "japanese": "ja",
    "korean": "ko",
    "arabic": "ar"
}

def translate_text(text, target_lang="english"):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise Exception("Missing OpenRouter API key")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Voice of the City"
    }

    prompt = f"Translate the following text to {target_lang.title()}:\n\n{text}"

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful translator."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"OpenRouter Translation Error: {response.status_code} - {response.text}")
