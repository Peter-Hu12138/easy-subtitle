from django.db import models
from django.db.models import TextField
from django.db.models.fields import CharField, IntegerField


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = {
        "IPR": "In progress",
        "PROC": "Under processing",
        "FAL": "Failed",
        "SUCC": "Successful"
    }
    uuid = CharField(max_length=100, unique=True)
    status = CharField(max_length=5, choices=STATUS_CHOICES, default="IPR")
    srt_content = TextField()
    created_at = models.DateTimeField(auto_now_add=True)
