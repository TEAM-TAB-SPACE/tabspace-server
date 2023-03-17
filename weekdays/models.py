from django.db import models


class Weekday(models.Model):
    month = models.CharField(max_length=2, blank=False, null=False)
    days = models.CharField(max_length=250, blank=False, null=False)
    korean_holidays = models.CharField(max_length=250, blank=False, null=False)
    
