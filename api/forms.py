from django.forms import ModelForm
from .models import Task

class FileUploadForm(ModelForm):
    class Meta:
        model = Task
        fields = ["audio_file"]
