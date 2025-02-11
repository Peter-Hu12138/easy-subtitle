from django.urls import path
from .views import *

urlpatterns = [
   # path("publish_works", publish_works, name="publish_works"),
    path('task', task, name="task"),
    path('task/<int:id>', task_status, name="task_status"),
    path("", testing_template, name="template")
]
