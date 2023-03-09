from django.shortcuts import render
import pandas as pd
import random
from .models import Lecture
from django.http import HttpResponse, Http404
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from datetime import datetime
import requests
from dateutil.relativedelta import *
from . import serializers 

class ProductsView(APIView):
    def get(self, request):
        lectures = Lecture.objects.all()
        serializer = serializers.LectureSerializer(lectures, many=True)
        return Response(status=status.HTTP_200_OK,data=serializer.data)


"""
db값 추가
"""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import os
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRET_BASE_FILE = os.path.join(BASE_DIR, 'lectures.csv')

def dbCreateView(request):

    db = pd.read_csv(SECRET_BASE_FILE, encoding='cp949')

    for i in range(0,len(db)):
        title = db['title'][i]
        category = db['category'][i]
        teacher = db['teacher'][i]
        duration = db['duration'][i]
        videoId = db['videoId'][i]              
        
        Lecture.objects.create(title=title, category=category, teacher=teacher, duration=duration,videoId=videoId)
    return HttpResponse('새로운 data가 저장되었습니다')  
     
def dbUpdateActiveView(request):
    lectures = Lecture.objects.filter(today_lecture = 1)
    for lecture in lectures:
        lecture.today_lecture = 0
        lecture.save()
    now = datetime.now()
    now = now.strftime('%Y%m%d')
    lectures = Lecture.objects.filter(date=now) #오늘날짜와 date가 일치하는 강의 리스트 = 오늘의 강의
    first_id = lectures[0].id #오늘의 강의 중 마지막 lecture.id
    last_id = lectures[len(lectures)-1].id #오늘의 강의 중 마지막 lecture.id
    for lecture in lectures:
        lecture.today_lecture = 1
        lecture.save()
    for i in range(first_id,last_id+1):
        lecture = Lecture.objects.get(id=i)
        lecture.active_lecture = 1
        lecture.save()
    
    return HttpResponse('오늘 강의가 업데이트 되었습니다')  

def dbUpdateView(request):
    for i in range(1,70):
        lecture = Lecture.objects.get(id=i)
        lecture.active = 0
        lecture.save()

    return HttpResponse('data가 수정되었습니다')  

def dbDateUpdateView(request):
    today = datetime.today()
    this_year = today.year
    this_month = today.month
    if len(str(this_month)) == 1:
        m = '0'+str(this_month)
    else:
        m = str(this_month)
    holidays = []
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo?_type=json'
    params ={'serviceKey' : 'PqcWn/nPR+ufv4dxJ4yYu3mlKif40gyMU4BInANpycnVthrB5PJiBmsSAe/kGkwDGAkINzK/KkEvi9XB140EFQ==', 'pageNo' : '1', 'numOfRows' : '10', 'solYear' : str(this_year), 'solMonth' : m }

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
    print(holidays)


    next_month = datetime(this_year, this_month, 1) + relativedelta(months=1)
    this_month_last = next_month + relativedelta(seconds=-1)
    this_month_last_day = this_month_last.strftime('%d')
    days = []


    for i in range(1, int(this_month_last_day)):
        day = datetime(this_year,this_month,i).weekday()
        
        if day!=5 and day!=6:
            if len(str(i)) == 1:
                d = '0'+str(i)
            else : 
                d = str(i)
            day_temp = f'{this_year}{m}{d}'
            if day_temp not in holidays:
                days.append(day_temp)
            

    lenture_num = 69
    lecture_days = []
    if lenture_num%(3*len(days)) == 0:
        for day in days:
            lecture_days.extend([day, day, day])
    else:
        remain = lenture_num%(3*len(days))
        for day in days[0:-remain]:
            lecture_days.extend([day, day, day])
        for day in days[-remain:]:
            lecture_days.extend([day, day, day, day]) 
    print(lecture_days)
    
    for i in range(1,70):
        lecture = Lecture.objects.get(id=i)
        lecture.date = lecture_days[i-1]
        lecture.save()
    
    return HttpResponse('강의 date가 수정되었습니다')  

def dbPkResetView(request):
    records = Lecture.objects.all()
    index = 1
    for record in records:
        old_record = Lecture.objects.get(id=record.id)
        record.id = index
        old_record.delete()
        record.save()        
        index = index + 1
    return HttpResponse('pk 값이 reset되었습니다.')