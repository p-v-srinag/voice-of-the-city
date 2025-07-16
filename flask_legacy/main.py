from flask import Flask
from dotenv import load_dotenv  # ✅ Load .env support
import os

from app.routes.routes import audio_route

# ✅ Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.register_blueprint(audio_route)

@app.route('/')
def home():
    return "🎙️ Voice of the City AI is running!"

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)

