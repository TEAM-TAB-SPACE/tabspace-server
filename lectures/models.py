from django.db import models
from config import settings


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=10)
    teacher = models.CharField(max_length=20)
    duration = models.PositiveIntegerField()
    videoId = models.CharField(max_length=100)
    date = models.CharField(blank=True, null=True,max_length=8,help_text='yyyymmdd')
    today_lecture = models.BooleanField(default=False, null=False)
    active_lecture = models.BooleanField(default=False, null=False)
    def __str__(self):
        return self.title

# 오늘 날짜랑 시간비교해서 active 여부 정하기
# 평일 계산해서 넣기 