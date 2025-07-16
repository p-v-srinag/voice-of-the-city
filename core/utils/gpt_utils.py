import os
import requests
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def generate_story(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Voice of the City"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # Free-tier model
        "messages": [
            {"role": "system", "content": "You are a friendly local storyteller and city guide."},
            {"role": "user", "content": f"User said: {user_input}\nRespond with a short, immersive local story or suggestion."}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"OpenRouter Error: {response.status_code} - {response.text}")
