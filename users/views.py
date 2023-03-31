from . import serializers
import requests
from .models import User
# from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt import views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
# from django.conf import settings
from config import settings
from django.utils import timezone
from secretkeys.models import SecretKey
from django.http import Http404
from lecture_rooms.models import LectureRoom
from lectures.models import Lecture, LectureCategory
from dashboards.models import Dashboard, UserGrowth
from homeworks.models import Homework, Submission
from django.contrib.auth import authenticate
from weekdays.models import Weekday
from datetime import datetime
from .func import update_user_notifications, submit_homeworks
from django.db.models import Max, Min, Avg


def get_tokens_for_user(user):
    
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def login(user):

    tokens = get_tokens_for_user(user)
    res = Response()
    serializer = serializers.UserIdSerializer(user)
    res.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE'],
        value=tokens["access"],
        expires=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
    res.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        value=tokens["refresh"],
        expires=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    res.data = {"Success" : "Login successfully","tokens":tokens, "user":serializer.data}  
    
    res.status=status.HTTP_200_OK
    
    return res

def kakao_access(request):
    serializer = serializers.KakaoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    auth_code = serializer.validated_data["code"]
    
    kakao_token_api = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.KAKAO_REST_API_KEY,
        'redirection_uri': 'http://localhost:3000/oauth/callback/kakao',
        'code': auth_code
    }

    token_response = requests.post(kakao_token_api, data=data).json()
    if token_response.get('error'):
        raise Http404
    
    access_token = token_response.get('access_token')
   

    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    
    kakao_id = user_info_response.json()['id']
    
    
    return kakao_id

@decorators.permission_classes([permissions.IsAuthenticated])
class UserNameView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            serializer = serializers.UserIdSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)  
        except User.DoesNotExist:
            return Response(data='This user does not exist', status=status.HTTP_404_NOT_FOUND)  
                
    
class KakaoRegisterView(APIView) :
    
    def post(self, request):
                    
        kakao_id = kakao_access(request)  
    
        if not 'realname' in request.data:
            try:
                User.objects.get(username='1'+str(kakao_id))
                user = User.objects.get(username='1'+str(kakao_id))
                user.last_login = timezone.now()
                user.save()
            
                return login(user) 
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND, data='This user does not exist')                                
        try:
            User.objects.get(username='1'+str(kakao_id))
            user = User.objects.get(username='1'+str(kakao_id))
            user.last_login = timezone.now()
            user.save()
          
            return login(user) 
        except User.DoesNotExist: 
              
            request_data_copy = request.data.copy()            
            request_data_copy['username'] = '1'+str(kakao_id)                 
            serializer = serializers.UserRegisterSerializer(data=request_data_copy)
            
            serializer.is_valid(raise_exception=True)
            req_key = serializer.validated_data['secret_key']
          
            try: 
                req_secret = SecretKey.objects.get(key=req_key)
                
                if serializer.validated_data['realname'] == req_secret.master and serializer.validated_data['phone'] == req_secret.phone and req_secret.active ==1:
                    serializer.save()              ##유저가입
                    req_secret.active = 0          
                    req_secret.save()              ##시크릿키 inactive 처리
                    
                    ##개강일 이후 가입할 경우를 위한 이전 출석에 대한 처리
            
                    this_month_weekdays = Weekday.objects.last()
                    weekdays = this_month_weekdays.days.split(',')
                    holidays = this_month_weekdays.korean_holidays.split(',')
                    
                    now = int(datetime.now().strftime('%d')) 
                    attendance = ''
                    for day in weekdays:
                        if int(day) < now :
                            if day in holidays:
                                attendance += 'h'
                            else:
                                attendance += '0'
                        elif int(day) >= now :
                            break
                    # print(attendance)    
                    user_id = serializer.data['id']
                    user = User.objects.get(id=user_id)
                    
                    Dashboard.objects.create(user=user, attendance=attendance, notifications='탭스페이스 입과를 환경합니다 (12) 오늘부터 탭탭이와 달려봐요 (6)')  ##유저 대시보드 생성
                    
                    for lecture in Lecture.objects.all().order_by('id'):
                        LectureRoom.objects.create(user=user, lecture=lecture)
                                        
                    dashboard = Dashboard.objects.get(user_id = user_id)
                    for lecture_category in LectureCategory.objects.all().order_by('id'):
                        UserGrowth.objects.create(lecture_category=lecture_category, dashboard=dashboard)
                    for homework in Homework.objects.all().order_by('id'):
                        Submission.objects.create(dashboard=dashboard, homework=homework)
                    
                    user.last_login = timezone.now()
                    user.save()
                    # login(user) 
                    # return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
                    return login(user)
                    
                elif serializer.validated_data['realname'] != req_secret.master: 
                    return Response(data='key user unmatched', status=status.HTTP_400_BAD_REQUEST)
                elif serializer.validated_data['phone'] != req_secret.phone: 
                    return Response(data='key phone unmatched', status=status.HTTP_400_BAD_REQUEST)
                elif req_secret.active ==0: 
                    return Response(data='inactive key', status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except SecretKey.DoesNotExist:
                return Response(data='this key does not exist', status=status.HTTP_400_BAD_REQUEST)
             
             
class CookieTokenRefreshSerializer(jwt_serializers.TokenRefreshSerializer):
    
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        print(attrs['refresh'])
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise jwt_exceptions.InvalidToken(
                'No valid token found in cookie \'refresh\'')
            
import random            
class GuestLoginView(APIView) :
    
    def post(self, request):
        
        if not 'mode' in request.data:
            return Response(data='mode is required', status=status.HTTP_400_BAD_REQUEST)
        
        latest_username_num = User.objects.latest('date_joined').username[-3:]
        username_num = int(latest_username_num) + 1
        username_num = '0'*(3 - len(str(username_num))) + str(username_num)
        username = f'guest{username_num}'
        
        if request.data['mode'] == 1:   #루피
            mode = 1
            User.objects.create(username=username, realname='모범생루피')  ##모범생 유저 생성        

        elif request.data['mode'] == 2:   #뽀로로   
            mode = 2
            User.objects.create(username=username, realname='노는게제일좋은뽀로로')  ##불량 유저 생성  

                    
        ##개강일 이후 가입할 경우를 위한 이전 출석에 대한 처리

        this_month_weekdays = Weekday.objects.last()
        weekdays = this_month_weekdays.days.split(',')
        holidays = this_month_weekdays.korean_holidays.split(',')    
        
        user = User.objects.get(username=username)
        user_id = user.id
        realname = user.realname
        
        for lecture in Lecture.objects.all().order_by('id'):
            LectureRoom.objects.create(user=user, lecture=lecture)   
        
        
        now = int(datetime.now().strftime('%d')) 
        
        if now == 1:           #오늘이 1일 일 때
            attendance = ''    
            Dashboard.objects.create(user=user, attendance=attendance, notifications='탭스페이스 입과를 환경합니다 (12) 오늘부터 탭탭이와 달려봐요 (6)')  ##유저 대시보드 생성                               
            dashboard = Dashboard.objects.get(user_id = user_id)
            for lecture_category in LectureCategory.objects.all().order_by('id'):
                UserGrowth.objects.create(lecture_category=lecture_category, dashboard=dashboard)
            for homework in Homework.objects.all().order_by('id'):
                Submission.objects.create(dashboard=dashboard, homework=homework)
            
            user.last_login = timezone.now()
            user.save()
            # login(user) 
            # return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
            return login(user)
        
        today_lecture = Lecture.objects.filter(today_lecture = 1).aggregate(id=Min('id'))
        today_lecture_id = today_lecture['id']
        lecture_room = LectureRoom.objects.filter(user=user)
        
        attendance = ''
        if mode == 1:
            for day in weekdays:
                if int(day) < now :
                    if day in holidays:
                        attendance += 'h'
                    else:
                        attendance += '1'
                elif int(day) >= now :
                    break
            lecture_room.filter(lecture_id__lt = today_lecture_id).update(completed = True, progress = 100)
            last_lecture_room = lecture_room.last()
            last_lecture_room.playtime = 1
            last_lecture_room.save()
            
        elif mode == 2:
            for day in weekdays:
                if int(day) < now :
                    if day in holidays:
                        attendance += 'h'
                    elif int(day) == now-1 :
                        attendance += '0'
                    else:
                        attendance += random.choice(['1','1','1','1','1','0'])
                elif int(day) >= now :
                    break
            attendence_wo_holiday = attendance.replace('h','')
            attendence_wo_holiday = list(attendence_wo_holiday)
            lectures = Lecture.objects.all()
            lecture_dates = lectures.distinct().values_list('date', flat=True)
            print(lecture_dates) 
            true_attendence_index = [i for i in range(0,len(attendence_wo_holiday)) if attendence_wo_holiday[i] == '1']
            true_lecture_dates = [lecture_dates[i] for i in true_attendence_index]
            true_lectures = Lecture.objects.filter(date__in=true_lecture_dates)
            print(true_lecture_dates)
            print(true_lectures)
            lecture_room = LectureRoom.objects.filter(lecture__in = true_lectures)
            print(lecture_room)
            lecture_room.update(completed = True, progress = 100)
            
        # print(attendance)    
        
        
        Dashboard.objects.create(user=user, attendance=attendance, notifications='')  ##유저 대시보드 생성
        
        msg = update_user_notifications(user_id, realname)
        dashboard = Dashboard.objects.get(user_id=user_id)
        dashboard.notifications = msg 
        dashboard.save()
        
        import math 
        for lecture_category in LectureCategory.objects.all().order_by('id'):
            lectures = Lecture.objects.filter(category = lecture_category)
            ability = math.ceil(100*len(lecture_room.filter(completed=1, lecture__in = lectures))/len(lectures))
            UserGrowth.objects.create(lecture_category=lecture_category, dashboard=dashboard, ability=ability)
        for homework in Homework.objects.all().order_by('id'):
            Submission.objects.create(dashboard=dashboard, homework=homework)
        if mode == 1:
            submission_id = Submission.objects.get(dashboard=dashboard, homework_id=7).id
            submit_homeworks(user_id, submission_id)
        user.last_login = timezone.now()
        user.save()
        # login(user) 
        # return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
        return login(user)
        

                
            

class CookieTokenRefreshView(jwt_views.TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("access"):
            # res = Response()
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                value=response.data["access"],
                expires=int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()),
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN'],
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
            # response.data = {"Success"}
            # del response.data["refresh"]
            # return response
        # response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)
    
    
                   
@decorators.permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    def post(self, request):
        try:
            
            refreshToken = request.COOKIES.get('refresh')
            
            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE'],
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
                )
            res.delete_cookie(
                key = settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
                domain=settings.SIMPLE_JWT['AUTH_COOKIE_DOMAIN']
                )
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            # res["X-CSRFToken"]=None
            res.data = {"Success" : "Logout successfully"}
                        
            return res
        except:
            raise exceptions.ParseError("Invalid token")
        
        
class KakaoRegisterValidationView(APIView) :
    
     def post(self, request):                
        serializer = serializers.UserRegisterValidationSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        req_key = serializer.validated_data['secret_key']
       
        try: 
            req_secret = SecretKey.objects.get(key=req_key)
            
            if serializer.validated_data['realname'] == req_secret.master and serializer.validated_data['phone'] == req_secret.phone and req_secret.active ==1:
                return Response(data=serializer.validated_data, status=status.HTTP_200_OK)  
            elif serializer.validated_data['realname'] != req_secret.master: 
                return Response(data={"secret_key":['key user unmatched']}, status=status.HTTP_400_BAD_REQUEST)
            elif serializer.validated_data['phone'] != req_secret.phone: 
                return Response(data={"secret_key":['key phone unmatched']}, status=status.HTTP_400_BAD_REQUEST)
            elif req_secret.active ==0: 
                return Response(data={"secret_key":['inactive key']}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SecretKey.DoesNotExist:
            return Response(data={"secret_key":['this key does not exist']}, status=status.HTTP_400_BAD_REQUEST)
        
        
"""
admin page login
"""
class StaffLoginView(APIView):
    def post(self, request):
        try: 
            if not 'username' in request.data or not 'password' in request.data:
                raise exceptions.ParseError('username and password are required')
            user = authenticate(username=request.data['username'], password=request.data['password'])
            if user is None:
                return Response(data='username or password is invalid', status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username = request.data['username'], is_staff = True)
            user.last_login = timezone.now()
            user.save()
            
            return login(user)
            
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)