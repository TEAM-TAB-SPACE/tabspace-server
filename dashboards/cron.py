from lectures.models import Lecture
from datetime import datetime
import requests
from dateutil.relativedelta import *
from users.models import User
from lecture_rooms.models import LectureRoom
from dashboards.models import Dashboard

def update_user_attendance():
    
    today_lectures = Lecture.objects.filter(today_lecture = 1)
    if len(today_lectures) == 0:
        for user in User.objects.all():
            Dashboard.objects.get(user=user).attendance += 1
        print('today is holiday')
    else:        
        for user in User.objects.all():
            completed_lectures = LectureRoom.objects.filter(user=user, lecture__in = today_lectures, completed = True)
        
            if len(completed_lectures) == len(today_lectures):
                Dashboard.objects.get(user=user).attendance += 1
            else:
                Dashboard.objects.get(user=user).attendance += 0
    
        print('attendance was updated')
    
  
 