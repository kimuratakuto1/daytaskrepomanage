from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class TaskTemplate(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_daily = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_done = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)
    template = models.ForeignKey(TaskTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.date}"
    
class Report(models.Model):
    date = models.DateField()
    content = models.TextField(default='名無しのタイトル')
    is_locked = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}の日報"