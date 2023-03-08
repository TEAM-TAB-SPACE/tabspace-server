from .models import Lecture
from datetime import datetime


def update_today_lectures():
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
    print(f'{datetime.now()}:오늘의 강의 업데이트 완료')