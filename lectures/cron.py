from .models import Lecture
from datetime import datetime
import requests
from dateutil.relativedelta import *
from weekdays.models import Weekday
from config import settings


def update_today_lectures():
    try:
        Lecture.objects.filter(today_lecture = 1).update(today_lecture = 0) #어제의 today값 수정
    except:
        print('There is no today lecture yesterday')
    
    now = datetime.now()
    now = now.strftime('%Y%m%d')
    try:
        Lecture.objects.filter(date=now).update(today_lecture = 1, active_lecture = 1) #오늘날짜와 date가 일치하는 강의 리스트 = 오늘의 강의
        print(f"{datetime.now()}:today's lecture updated")
        
    except:
        print(f"{datetime.now()}:there is no today's lecture")   
    
def update_no_today_lectures():
    try:
        Lecture.objects.filter(today_lecture = 1).update(today_lecture = 0) #어제의 today값 수정
        print(f"{datetime.now()}:today's lecture updated")

        
    except:
        print(f"{datetime.now()}:there is no today's lecture")   
    

    
def update_monthly_lectures():
    #이번달 공휴일 계산
    
    today = datetime.today()
    this_year = today.year
    this_month = today.month
    if len(str(this_month)) == 1:
        m = '0'+str(this_month)
    else:
        m = str(this_month)
    holidays = []
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json'
    params ={'serviceKey' : settings["KOREAN_API_KEY"], 'pageNo' : '1', 'numOfRows' : '10', 'solYear' : str(this_year), 'solMonth' : m }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        response = requests.get(url, params=params).json()
        try:
            holidays_data = response['response']['body']['items']['item']
            for holiday in holidays_data:
                holidays.append(str(holiday['locdate']))
        except:
            holidays_data = response['response']['body']['items']['item']
            holidays.append(str(holidays_data['locdate']))
    


    next_month = datetime(this_year, this_month, 1) + relativedelta(months=1)
    this_month_last = next_month + relativedelta(seconds=-1)
    this_month_last_day = this_month_last.strftime('%d')
    days = []
    weekdays = ''

    for i in range(1, int(this_month_last_day)+1):
        day = datetime(this_year,this_month,i).weekday()
        
        if day!=5 and day!=6:
            weekdays += f'{i},'  # for weekdays app
            
            if len(str(i)) == 1:
                d = '0'+str(i)
            else : 
                d = str(i)
            day_temp = f'{this_year}{m}{d}'
            if day_temp not in holidays:
                days.append(day_temp)
                
    # for weekdays app
    weekdays = weekdays[:-1]
    
    holidays2 = ''
    for holiday in holidays:
        
        if holiday[-2] == '0':
            holidays2 += f'{holiday[-1]},'
        else:
            holidays2 += f'{holiday[-2:]},'
    holidays2 = holidays2[:-1]
    
    weekday = Weekday.objects.last()
    weekday.month=this_month
    weekday.days=weekdays
    weekday.korean_holidays=holidays2
    weekday.save()
    
    
            
    # for lectures app
    lecture_num = len(Lecture.objects.all())
    lecture_days = []
    if lecture_num%(3*len(days)) == 0:
        for day in days:
            lecture_days.extend([day, day, day])
    else:
        remain = lecture_num%(3*len(days))
        for day in days[0:-remain]:
            lecture_days.extend([day, day, day])
        for day in days[-remain:]:
            lecture_days.extend([day, day, day, day]) 
    # print(lecture_days)
    
    for i in range(1,lecture_num+1):
        lecture = Lecture.objects.get(id=i)
        lecture.date = lecture_days[i-1]
        lecture.save()
    try:
        Lecture.objects.filter(today_lecture = 1).update(today_lecture = 0) #어제의 today값 수정
        Lecture.objects.all().update(active_lecture = 0)
        now = datetime.now()
        now = now.strftime('%Y%m%d')
        Lecture.objects.filter(date=now).update(today_lecture = 1, active_lecture = 1)
        print(f'{datetime.now()}:monthly lecture updated')
    except:
        print(f'{datetime.now()}:monthly lecture updated, but there is no lecture today')
    
    
def test():
    print('test')
