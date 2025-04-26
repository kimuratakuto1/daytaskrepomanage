from django.contrib import admin
from .models import Task,TaskTemplate

admin.site.register(Task)
admin.site.register(TaskTemplate)