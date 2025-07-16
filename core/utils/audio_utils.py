import whisper
import uuid
from gtts import gTTS
import os
import tempfile

# Load Whisper model once
model = whisper.load_model("base")

def transcribe_audio(file):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    return result['text']

def speak_text(text):
    filename = f"core/static/audio/story_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text)
    tts.save(filename)
    return filename
