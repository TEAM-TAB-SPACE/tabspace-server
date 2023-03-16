from django.db import models

class Dashboard(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    attendance = models.CharField(max_length=50, blank=True, null=True)
    homework_progress = models.PositiveIntegerField(default=0, null=False)
    # latest_lecture = models.CharField(max_length=100, blank=True, null=True)
    
class UserGrowth(models.Model):
    lecture_category = models.ForeignKey('lectures.LectureCategory', on_delete=models.CASCADE)
    dashboard = models.ForeignKey('dashboards.Dashboard', on_delete=models.CASCADE)
    ability = models.PositiveIntegerField(default=0, null=False)