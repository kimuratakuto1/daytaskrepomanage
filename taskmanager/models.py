from django.db import models
from django.utils import timezone

class TaskTemplate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_daily = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    template = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.date}"