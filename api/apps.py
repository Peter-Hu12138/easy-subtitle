from django.apps import AppConfig
from django.db.models import Q
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from utils.formatting import seconds_to_str_in_srt
import os, json
import io
from openai import OpenAI
from openai.types.audio import Translation, TranslationVerbose, TranslationCreateResponse
from utils.chunking import chunk
import threading
import time

l = threading.Lock()
RUN = True

def run_background_task():
    from .models import Task
    while True:
        time.sleep(10)

        # get a job
        l.acquire()
        task_to_deal_with = Task.objects.filter(status="IPR").order_by("created_at").first()
        if task_to_deal_with:
            task_to_deal_with.status = "PROC"
        l.release()

        # deal_task
        if task_to_deal_with:
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
            # update the model: change status and
        else:
            pass

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Start a separate thread when the app is ready
        if RUN:
            thread_1 = threading.Thread(target=run_background_task)
            thread_1.start()
            thread_2 = threading.Thread(target=run_background_task)
            thread_2.start()
