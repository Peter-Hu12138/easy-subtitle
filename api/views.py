from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from utils.formatting import seconds_to_str_in_srt
import os, json
import io
from openai import OpenAI
from openai.types.audio import Translation, TranslationVerbose, TranslationCreateResponse
from utils.chunking import chunk

# Create your views here.
def task(request: HttpRequest):
    file_name_uploaded = "fileInput"
    file = request.FILES[file_name_uploaded]
    if file.size <= 1024 * 1024 * 100:
        file_data = file.read()
    else:
        # need chunking for extremely large files
        # or raise an error
        raise Exception

    audio_list, len_list = chunk(file_data)

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )

    last_segment_ended_at = 0
    index = 1
    srt_str = ""
    for i in range(len(audio_list)):
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=("temp.mp3", audio_list[i], "audio/mp3"),
            timestamp_granularities="segment",
            response_format="verbose_json",
        )

        transcription_data = transcription.to_dict()

        for line_segment in transcription_data["segments"]:
            start = last_segment_ended_at + line_segment["start"]
            end = last_segment_ended_at + line_segment["end"]
            segment_text = line_segment["text"].strip()
            start = seconds_to_str_in_srt(start)
            end = seconds_to_str_in_srt(end)
            srt_str += f"{index} \n{start} --> {end} \n{segment_text}\n\n"
            index += 1
        last_segment_ended_at += len_list[i]
    response = JsonResponse({})
    response.write(srt_str)
    return response

def task_status(request: HttpRequest):
    pass
# from pydub import AudioSegment

def testing_template(request):
    return render(request, "testing_template.html", {})
