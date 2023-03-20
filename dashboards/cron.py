from lectures.models import Lecture
from datetime import datetime
import requests
from dateutil.relativedelta import *
from users.models import User
from lecture_rooms.models import LectureRoom
from dashboards.models import Dashboard
from weekdays.models import Weekday
from homeworks.models import Homework
from homeworks.models import Submission


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

def update_user_notifications():
    
    today = datetime.today().strftime('%y%m%d')
    today = f'20{today}'
    this_month_weekdays = Weekday.objects.last()
    this_year = int(today[0:4])
    this_month = int(this_month_weekdays.month)
    weekdays = this_month_weekdays.days.split(',')
    holidays = this_month_weekdays.korean_holidays.split(',')
    
    weeks = {}
    week = []
    week_num = 1
    for day in weekdays:
        week.append(day)   
        if datetime(this_year,this_month,int(day)).weekday() == 4 or day == weekdays[-1]:       
            weeks[week_num] = week
            week = []
            week_num +=1
    print(weeks)
    week_num = list(weeks.keys()) 
    print(week_num)
           
    
    today = today[-2:]
    # 개강알림
    if today == weeks[1][0]:
        Dashboard.objects.all().update(notifications = '오늘은 탭스페이스 1기 프론트엔드 과정 개강일입니다 ~ 이제부터 탭탭이와 함께 달려보아요 ! ◡( ๑❛ᴗ❛ )◡')       
        return print('notification updated')
    # 종강알림
    if today == weeks[week_num[-1]][-1]:
        Dashboard.objects.all().update(notifications = '오늘은 탭스페이스 1기 프론트엔드 과정 종강일입니다 ~ 그 동안 고생 많으셨습니다 ! 강의평가도 참여 부탁드려요 (人^з^)-☆')       
        return print('notification updated')
    #공휴일일 때 알림
    if today in holidays:
        Dashboard.objects.all().update(notifications = '탭탭이와 함께하는 즐거운 공휴일 (✿◠‿◠)')
        return print('notification updated')
    #주말일 때 알림
    if datetime(this_year,this_month,int(today)).weekday() in [5,6]:
        Dashboard.objects.all().update(notifications = '탭탭이와 함께하는 즐거운 주말 (*●⁰ꈊ⁰●)ﾉ')
        return print('notification updated')
    #개인알림
    
    active_lectures = Lecture.objects.filter(active_lecture = True)
    today_lectures = Lecture.objects.filter(today_lecture = True)
    for dashboard in Dashboard.objects.all():
        msg = []
        user_name = dashboard.user
        
        #월요일, 금요일 알림
        if datetime(this_year,this_month,int(today)).weekday() == 0:
            msg.append('탭탭이와 함께 월요병을 날려보아요 (/◕ヮ◕)/')
        elif datetime(this_year,this_month,int(today)).weekday() == 5:
            msg.append('드디어 금요일 ! 한주의 마무리를 탭탭이와 함께해요 ⸜(*ˊᗜˋ*)⸝')
            
        #출석관련 알림
        if dashboard.attendance[-1] == '0':  #전날 결석일 때 알림
            msg.append(f'{user_name}님 돌아오셨군요 ! 오늘은 열심히 저와 함께 달려보아요 ! ₍₍ (ง ˘ω˘ )ว ⁾⁾')
            if dashboard.attendance.count('0') >= 1:
                msg.append(f'총 {dashboard.attendance.split().count("0")}번 결석하셨어요. 결석이 3번 이상이면 불이익이 발생할 수 있어요 ( ఠ్ఠ ˓̭ ఠ్ఠ )')            
        elif not '0' in dashboard.attendance:
            msg.append(f'{user_name}님의 성실함이 눈부셔요 !! 이대로만 계속 가요 ദ്ദിㆁᴗㆁ✿)')           
        
        #강의 수강 독려 알림 
        try:      
            uncompleted_lecture_rooms = LectureRoom.objects.filter(user=user_name, lecture__in = active_lectures, completed = False)
            if len(uncompleted_lecture_rooms) > len(today_lectures):
               msg.append('오늘은 밀린 강의를 청소해 볼까요 ? 마음이 한결 가벼워질거에요 ٩(ˊᗜˋ*)و') 
        except LectureRoom.DoesNotExist:
            msg.append('밀린 강의 == ZERO ✧')    
        
        total_homework = len(Homework.objects.all())
        try: 
            completed_submission = len(Submission.objects.filter(dashboard=dashboard, is_submitted =True))
            print(completed_submission)
        except Submission.DoesNotExist:
            completed_submission = 0
        # if today in weeks[week_num[0]] : #첫주
        #     continue
            
        # elif today in weeks[week_num[1]] : #둘째주
        #     continue
            
        if today in weeks[week_num[2]] : #셋째주
            if completed_submission == 0:
                msg.append('이제는 과제를 시작해야할 때  (୨୧ ❛ᴗ❛)✧')
            elif completed_submission == 1:
                msg.append('과제 1개만 더 힘내봐요 (/◕ヮ◕)/')
                
        elif today in weeks[week_num[-1]] : #마지막주
            if completed_submission == 0:
                msg.append('마지막 선물로 탭탭이에게 과제를 제출해 주세요 (/◕ヮ◕)/')
            elif completed_submission == (total_homework-1):
                msg.append('과제 1개만 더 힘내봐요 ! (/◕ヮ◕)/')
            elif completed_submission == total_homework:
                msg.append('모든 과제를 제출하셨군요 대단해요 ദ്ദി(⩌ᴗ⩌ )')
            else:
                msg.append('아직 완료하지 못한 과제가 남아있어요 ! 힘내봐요 (੭˙ ˘ ˙)੭')
                
        elif today in weeks[week_num[-2]] : #넷째주
            if completed_submission == 0:
                msg.append('이제는 정말 과제를 시작해야할 때  (୨୧ ❛ᴗ❛)✧')
            elif completed_submission < (total_homework-1) :
                msg.append('탭탭이랑 1일 1과제 어때요 ?  ✦‿✦')
            elif completed_submission == (total_homework-1):
                msg.append('과제 1개만 더 힘내봐요 ! (/◕ヮ◕)/')
            else:
                msg.append('벌써 모든 과제를 제출하셨군요 대단해요 ദ്ദി(⩌ᴗ⩌ )')
        print(msg)
        msg = ','.join(msg)
        print(msg)
        dashboard.notifications = msg   
        dashboard.save()   
    print('notification updated')  
        
             

  
 
    
  
 