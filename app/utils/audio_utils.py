import whisper
from gtts import gTTS
import uuid
import os
import requests
import tempfile

# Load Whisper model once
model = whisper.load_model("base")

def transcribe_audio(file):
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    # Transcribe using Whisper
    result = model.transcribe(tmp_path)
    return result['text']


def generate_story(user_input):
    api_key = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  # required by OpenRouter
        "X-Title": "Voice of the City"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",  # Free model
        "messages": [
            {"role": "system", "content": "You are a local storyteller and city guide."},
            {"role": "user", "content": f"User said: {user_input}\nRespond with a short, immersive local story or suggestion."}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(f"OpenRouter Error: {response.status_code} - {response.text}")


def speak_text(text):
    filename = f"static/audio/story_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text)
    tts.save(filename)
    return filename
