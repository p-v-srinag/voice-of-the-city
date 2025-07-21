import whisper
from gtts import gTTS
import uuid
import os
import tempfile

model = whisper.load_model("base")

def transcribe_audio(file_obj):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file_obj.read())
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return result['text']

def speak_text(text):
    filename = f"core/static/audio/story_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text)
    tts.save(filename)
    return filename
