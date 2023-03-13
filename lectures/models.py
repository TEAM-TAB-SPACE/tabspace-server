from django.db import models
from config import settings


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey('lectures.LectureCategory', on_delete=models.CASCADE)
    teacher = models.CharField(max_length=20)
    duration = models.PositiveIntegerField()
    videoId = models.CharField(max_length=100)
    date = models.CharField(blank=True, null=True,max_length=8,help_text='yyyymmdd')
    today_lecture = models.BooleanField(default=False, null=False)
    active_lecture = models.BooleanField(default=False, null=False)
    def __str__(self):
        return self.title

class LectureCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name