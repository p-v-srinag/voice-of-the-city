from flask import Blueprint, request, jsonify
from app.utils.audio_utils import transcribe_audio, generate_story, speak_text

audio_route = Blueprint("audio_route", __name__)

@audio_route.route('/voice', methods=['POST'])
def handle_voice():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    print("📥 Received file:", audio_file.filename)

    try:
        print("🔍 Transcribing...")
        transcript = transcribe_audio(audio_file)

        print("🧠 Generating story...")
        story = generate_story(transcript)

        print("🔊 Converting to speech...")
        audio_path = speak_text(story)

        return jsonify({
            "transcription": transcript,
            "story": story,
            "audio_output_path": audio_path
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
