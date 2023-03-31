from datetime import datetime
from weekdays.models import Weekday
from lectures.models import Lecture
from dashboards.models import Dashboard
from lecture_rooms.models import LectureRoom
from homeworks.models import Submission, Storage
from users.models import User
import boto3
from config import settings



def update_user_notifications(user_id, realname):
    
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
    # print(weeks)
    week_num = list(weeks.keys()) 
    # print(week_num)
           
    ## 이모티콘 약속 : {'(1)': '😀', '(2)': '🥺','(3)': '🤓', '(4)': '🤗', '(5)': '😉', '(6)': '😎', '(7)': '🥰', '(8)': '😍', '(9)': '🥳', '(10)': '✨', '(11)': '🔥', '(12)': '🎉', '(13)': '🚗', '(14)': '👍'}
    today = today[-2:]
    
    msg = []
    # 개강알림
    if today == weeks[1][0]:
       msg.append('오늘은 탭스페이스 1기 프론트엔드 과정 개강일입니다 (12), 이제부터 탭탭이와 함께 달려보아요 ! (1)') 
       msg = ','.join(msg)      
       return msg
    # 종강알림
    if today == weeks[week_num[-1]][-1]:
        msg.append('오늘은 탭스페이스 1기 프론트엔드 과정 종강일입니다 (12), 그 동안 고생 많으셨습니다 ! 강의평가도 참여 부탁드려요 (7)')   
        msg = ','.join(msg)    
        return msg
    #공휴일일 때 알림
    if today in holidays:
        msg.append('탭탭이와 함께하는 즐거운 공휴일 (5), 공휴일에는 오늘의 강의가 없어요 (3), 완료하지 못한 강의와 숙제가 있다면 탭탭이와 함께 도전 (6)')
        msg = ','.join(msg)
        return msg
    #주말일 때 알림
    if datetime(this_year,this_month,int(today)).weekday() in [5,6]:
        msg.append('탭탭이와 함께하는 즐거운 공휴일 (5), 주말에는 오늘의 강의가 없어요 (3), 완료하지 못한 강의와 숙제가 있다면 탭탭이와 함께 도전 (6)')
        msg = ','.join(msg)
        return msg
    
    #개인알림
    
    active_lectures = Lecture.objects.filter(active_lecture = True)
    today_lectures = Lecture.objects.filter(today_lecture = True)
    dashboard = Dashboard.objects.filter(user_id = user_id)
    try:
        msg = []
        user_name = realname
        
        #월요일, 금요일 알림
        if datetime(this_year,this_month,int(today)).weekday() == 0:
            msg.append('탭탭이와 함께 월요병을 날려보아요 (1)')
        elif datetime(this_year,this_month,int(today)).weekday() == 5:
            msg.append('드디어 금요일 (11) 금요일도 탭탭이와 함께해요 (11) (11)')
            
        #출석관련 알림
        if dashboard.attendance[-1] == '0':  #전날 결석일 때 알림
            msg.append(f'{user_name}님 돌아오셨군요 ! 오늘은 열심히 저와 함께 달려보아요 ! (6)')
            if dashboard.attendance.count('0') >= 1:
                msg.append(f'총 {dashboard.attendance.count("0")}번 결석하셨어요. 결석이 5번 이상이면 불이익이 발생할 수 있어요 (2)')            
        elif not '0' in dashboard.attendance:
            msg.append(f'{user_name}님의 성실함이 눈부셔요 (10) 이대로만 계속 가요 (13) (13)')           
        
        #강의 수강 독려 알림 
        try:      
            uncompleted_lecture_rooms = LectureRoom.objects.filter(user=user_name, lecture__in = active_lectures, completed = False)
            if len(uncompleted_lecture_rooms) > len(today_lectures):
                msg.append('오늘은 밀린 강의를 청소해 볼까요 ? 마음이 한결 가벼워질거에요 (4)') 
        except LectureRoom.DoesNotExist:
            msg.append('밀린 강의 == ZERO (10)')    
        

        # if today in weeks[week_num[0]] : #첫주
        #     continue
            
        # elif today in weeks[week_num[1]] : #둘째주
        #     continue
            
        if today in weeks[week_num[2]] : #셋째주
            msg.append('이제는 과제를 시작해야할 때 (3)')
          
                
        elif today in weeks[week_num[-1]] : #마지막주
            msg.append('마지막 선물로 탭탭이에게 과제를 제출해 주세요 (4)')
           
                
        elif today in weeks[week_num[-2]] : #넷째주
            msg.append('이제는 정말 과제를 시작해야할 때 (3)')

    except:
        msg.append('아쉽게도 아직 개강일이 되지 않았어요 (2)', '개강일에 건강한 모습으로 만나요 (1)')
        # print(msg)
    msg = ','.join(msg)
    return msg
        # print(msg)
        
def submit_homeworks(user_id, submission_id):
    user_id = user_id
    # if not 'id' in request.data:
    #     raise exceptions.ParseError('error:"id" is required')   #submission id
    # if len(request.data)==1:
    #     raise exceptions.ParseError('error: there is no data to be updated')
    # print(request.data['file'])
    # if request.data['file'] == '':
    #     raise exceptions.ParseError('error: there is no data to be updated')
    
    submission = Submission.objects.get(id=submission_id)            
                
    user_uuid = User.objects.get(id=user_id).uuid
    
    # file_serializer = serializers.StorageFileSerializer(submission, request.data, partial=True)
    # file_serializer.is_valid(raise_exception=True)            
    
    s3 = boto3.client('s3')   
    
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent
    import os
    FILE = os.path.join(BASE_DIR, 'homework.py')
    file = open(FILE, 'rb')         
    now = datetime.now()
    now = now.strftime('%Y%m%d_%H%M%S')
    s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, f'{user_uuid}/{submission.id}/{now}_homework.py')
    
    s3_url = f"{settings.CLOUDFRONT}/{user_uuid}/{submission.id}/{now}_homework.py"
    
    
    Storage.objects.create(submission = submission, url = s3_url)
    
    if submission.is_submitted == False:
        submission.is_submitted = True
        submission.save()

    
    