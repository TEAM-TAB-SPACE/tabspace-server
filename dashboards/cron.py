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
        for user in User.objects.filter(is_superuser = False):
            dashboard = Dashboard.objects.get(user=user)
            dashboard.attendance += 'h'
            dashboard.save()
            
        print('today is holiday')
    else:        
        for user in User.objects.filter(is_superuser = False):
            
            completed_lectures = LectureRoom.objects.filter(user=user, lecture__in = today_lectures, completed = True)
            
            if len(completed_lectures) == len(today_lectures):
                
                dashboard = Dashboard.objects.get(user=user)
                dashboard.attendance += '1'
                dashboard.save()
                
            else:
            
                dashboard = Dashboard.objects.get(user=user)
                dashboard.attendance += '0'
                dashboard.save()
        print('attendance was updated')
         

  
 
    
  
 