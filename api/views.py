from datetime import timezone

from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from utils.formatting import seconds_to_str_in_srt
import os, json
import io
from openai import OpenAI
from openai.types.audio import Translation, TranslationVerbose, TranslationCreateResponse
from django.utils import timezone
from utils.chunking import chunk
from django.core.files.base import File
from . import models
from .forms import FileUploadForm


def task(request: HttpRequest):
    file_name_uploaded = "audio_file"
    file = request.FILES[file_name_uploaded]
    if 0 < file.size <= 1024 * 1024 * 100:  # validate that it is from a trusted source
        file_data = file.read()
    else:
        # need chunking for extremely large files
        # or raise an error
        raise Exception
    instance = models.Task()
    instance.uuid = f"test_{timezone.now().__str__()}"
    instance.audio_file.save(f"./audio/audio_{instance.uuid}.mp3", File(file), save=True)
    instance.save()
    return HttpResponse("SUCC")
    # audio_list, len_list = chunk(file_data)



def task_status(request: HttpRequest):
    pass
# from pydub import AudioSegment

def testing_template(request):
    return render(request, "testing_template.html", {})
