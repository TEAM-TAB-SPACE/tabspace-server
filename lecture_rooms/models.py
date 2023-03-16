from django.db import models
from common.models import CommonModel

class LectureRoom(CommonModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    lecture = models.ForeignKey('lectures.Lecture', on_delete=models.CASCADE)
    playtime = models.PositiveIntegerField(default=0, null=False)
    progress = models.PositiveIntegerField(default=0, null=False)
    endtime = models.PositiveIntegerField(default=0, null=False)
    is_clicked = models.BooleanField(default=0, null=False)
    completed = models.BooleanField(default=0, null=False)
   
    def __str__(self):
        return f'{self.user}-{self.lecture}'
