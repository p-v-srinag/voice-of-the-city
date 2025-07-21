from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from .utils.audio_utils import transcribe_audio, speak_text
from .utils.gpt_utils import generate_story
from .utils.lang_utils import translate_text, LANGUAGE_CODES
from gtts import gTTS
import os
import base64

LANGUAGES = list(LANGUAGE_CODES.keys())

@csrf_exempt
def home(request):
    if request.method == 'POST':
        transcription = story = translated = audio_path = error = None
        try:
            # Uploaded Audio
            if request.FILES.get('audio'):
                audio_file = request.FILES['audio']
                fs = FileSystemStorage(location='core/static/audio')
                filename = fs.save(audio_file.name, audio_file)
                filepath = fs.path(filename)
                with open(filepath, 'rb') as f:
                    transcription = transcribe_audio(f)

            # Real-time base64 audio
            elif request.POST.get('audio_base64'):
                audio_data = base64.b64decode(request.POST.get('audio_base64'))
                temp_path = 'core/static/audio/recorded.wav'
                with open(temp_path, 'wb') as f:
                    f.write(audio_data)
                with open(temp_path, 'rb') as f:
                    transcription = transcribe_audio(f)

            elif request.POST.get('text'):
                transcription = request.POST.get('text')

            else:
                raise Exception("No valid input provided.")

            story = generate_story(transcription)
            lang = request.POST.get('target_lang', 'english').lower()
            translated = translate_text(story, target_lang=lang)
            lang_code = LANGUAGE_CODES.get(lang, 'en')
            tts = gTTS(text=translated, lang=lang_code)
            output_path = os.path.join("core/static/audio", "output.mp3")
            tts.save(output_path)
            audio_path = '/' + output_path

        except Exception as e:
            error = str(e)

        return render(request, 'core/index.html', {
            "transcription": transcription,
            "story": story,
            "translated": translated,
            "audio_path": audio_path,
            "error": error,
            "languages": LANGUAGES,
        })

    return render(request, 'core/index.html', {"languages": LANGUAGES})


@csrf_exempt
def handle_voice(request):
    if request.method == 'POST':
        try:
            if request.FILES.get('audio'):
                audio_file = request.FILES['audio']
                fs = FileSystemStorage(location='core/static/audio')
                filename = fs.save(audio_file.name, audio_file)
                filepath = fs.path(filename)
                with open(filepath, 'rb') as f:
                    text = transcribe_audio(f)
                story = generate_story(text)
                audio_response_path = speak_text(story)
                return JsonResponse({
                    "transcription": text,
                    "story": story,
                    "audio_output_path": "/" + audio_response_path
                })

            elif request.POST.get("text"):
                user_input = request.POST.get("text")
                lang = request.POST.get("target_lang", "english")
                translated = translate_text(user_input, target_lang=lang)
                lang_code = LANGUAGE_CODES.get(lang.lower(), "en")
                tts = gTTS(text=translated, lang=lang_code)
                output_path = os.path.join("core/static/audio", "translated.mp3")
                tts.save(output_path)
                return JsonResponse({
                    "translated": translated,
                    "audio_output_path": "/" + output_path
                })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)
