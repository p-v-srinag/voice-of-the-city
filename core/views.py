from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .utils.audio_utils import transcribe_audio, speak_text
from .utils.gpt_utils import generate_story
from .utils.lang_utils import translate_text, LANGUAGE_CODES
from gtts import gTTS
import os

LANGUAGES = [
    "english", "hindi", "telugu", "tamil", "bengali", "marathi", "gujarati", "punjabi", "urdu", "kannada",
    "malayalam", "nepali", "french", "german", "spanish", "italian", "chinese", "japanese", "korean", "arabic"
]

@csrf_exempt
def home(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        fs = FileSystemStorage(location='core/static/audio')
        filename = fs.save(audio_file.name, audio_file)
        filepath = fs.path(filename)

        try:
            text = transcribe_audio(open(filepath, 'rb'))
            story = generate_story(text)
            audio_path = speak_text(story)

            return render(request, 'core/index.html', {
                "transcription": text,
                "story": story,
                "audio_path": '/' + audio_path,
                "languages": LANGUAGES
            })
        except Exception as e:
            return render(request, 'core/index.html', {
                "error": str(e),
                "languages": LANGUAGES
            })

    return render(request, 'core/index.html', {"languages": LANGUAGES})


@csrf_exempt
def handle_voice(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        fs = FileSystemStorage(location='core/static/audio')
        filename = fs.save(audio_file.name, audio_file)
        filepath = fs.path(filename)

        try:
            text = transcribe_audio(open(filepath, 'rb'))
            story = generate_story(text)
            audio_response_path = speak_text(story)

            return JsonResponse({
                "transcription": text,
                "story": story,
                "audio_output_path": "/" + audio_response_path
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST' and request.POST.get("text"):
        try:
            user_input = request.POST.get("text")
            lang = request.POST.get("target_lang", "en")
            translated = translate_text(user_input, target_lang=lang)
            target_lang_code = LANGUAGE_CODES.get(lang.lower(), "en")

            tts = gTTS(text=translated, lang=target_lang_code)
            output_path = os.path.join("core/static/audio", "translated.mp3")
            tts.save(output_path)

            return JsonResponse({
                "translated": translated,
                "audio_output_path": "/" + output_path
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
