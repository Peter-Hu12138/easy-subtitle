from datetime import timezone
import uuid
from django.core.exceptions import BadRequest
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

    if file.size <= 0 or file.size >= 1024 * 1024 * 100:  # check file size
        raise BadRequest
    # TODO: cloudflare captcha

    instance = models.Task()
    instance.uuid = str(uuid.uuid4())
    instance.audio_file.save("audio_" + instance.uuid + ".mp3", File(file), save=True)
    instance.save()

    return HttpResponse("SUCC")


def task_status(request: HttpRequest):
    pass
# from pydub import AudioSegment

def testing_template(request):
    return render(request, "testing_template.html", {})
