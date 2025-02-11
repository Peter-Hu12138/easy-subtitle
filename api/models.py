from django.db import models
from django.db.models.fields import CharField, IntegerField


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = {
        "IPR": "In progress",
        "FAL": "Failed",
        "SUCC": "Successful"
    }
    uuid = CharField(max_length=100, unique=True)
    status = CharField(choices=STATUS_CHOICES, default="IPR")
