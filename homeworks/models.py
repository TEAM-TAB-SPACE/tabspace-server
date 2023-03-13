from django.db import models
from common.models import CommonModel

class Homework(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    def __str__(self):
        return self.title

class Submission(CommonModel):
    dashboard = models.ForeignKey('dashboards.Dashboard', on_delete=models.CASCADE)
    homework = models.ForeignKey('homeworks.Homework', on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False, blank=False, null=False)
    url = models.CharField(max_length=100, null=True, blank=True)
    file = models.FileField(null=True, blank=True)