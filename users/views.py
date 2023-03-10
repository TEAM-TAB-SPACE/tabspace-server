from . import serializers
import requests
from .models import User
# from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
# from django.conf import settings
from config import settings
from django.utils import timezone
from secretkeys.models import SecretKey
from django.http import Http404
from lecture_rooms.models import LectureRoom
from lectures.models import Lecture, LectureCategory
from dashboards.models import Dashboard, UserGrowths
from homeworks.models import Homework, Submission

def get_tokens_for_user(user):
    
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def login(user):

    tokens = get_tokens_for_user(user)
    res = Response()
    serializer = serializers.UserSerializer(user)

    # res.data = tokens
    res.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
        value=tokens["refresh"],
        expires=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    res.data = {"Success" : "Login successfully","tokens":tokens, "realname":serializer.data['realname']}
   
    
    
    res.status=status.HTTP_200_OK
    
    return res

def kakao_access(request):
    serializer = serializers.KakaoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    auth_code = serializer.validated_data["code"]
    
    kakao_token_api = 'https://kauth.kakao.com/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': '2e1bc15f48ecb56bf87feef6738933b9',
        'redirection_uri': 'http://localhost:3000/oauth/callback/kakao',
        'code': auth_code
    }

    token_response = requests.post(kakao_token_api, data=data).json()
    if token_response.get('error'):
        raise Http404
    
    access_token = token_response.get('access_token')
    print(access_token)

    user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})
    # print(user_info_response.json())
    kakao_id = user_info_response.json()['id']
    print(kakao_id)
    
    return kakao_id


class KaKaoSignInCallBackView(APIView):
    def post(self, request):
        kakao_id= kakao_access(request)
                
        
        print(kakao_id)
        # print(error)
        
        
        try:
            user = User.objects.get(username='1'+str(kakao_id))
            print(user)
            user.last_login = timezone.now()
            user.save()
            # auth_login(request,user)
            print('login')
            
            return login(user)
            
        except User.DoesNotExist:
            # ????????? ????????? ????????? ????????? 400, ??????????????? ???????????? post??? ??????. post??? ???????????? ??????
            return  Response(status=status.HTTP_404_NOT_FOUND, data='this user does not exist')
    
class KakaoRegisterView(APIView) :
    
    def post(self, request):
        kakao_id = kakao_access(request)             
                             
        try:
            User.objects.get(username='1'+str(kakao_id))
            user = User.objects.get(username='1'+str(kakao_id))
            user.last_login = timezone.now()
            user.save()
            print('login')
            return login(user) 
        except User.DoesNotExist:   
            request_data_copy = request.data.copy()            
            request_data_copy['username'] = '1'+str(kakao_id)                 
            serializer = serializers.UserRegisterSerializer(data=request_data_copy)
            
            serializer.is_valid(raise_exception=True)
            req_key = serializer.validated_data['secret_key']
            print(req_key)
            try: 
                req_secret = SecretKey.objects.get(key=req_key)
                
                if serializer.validated_data['realname'] == req_secret.master and serializer.validated_data['phone'] == req_secret.phone and req_secret.active ==1:
        
                    print(serializer)
                    serializer.save()
                    req_secret.active = 0
                    req_secret.save()
                    print(serializer.data['id'])
                    
                    user_id = serializer.data['id']
                    user = User.objects.get(id=user_id)
                    for lecture in Lecture.objects.all().order_by('id'):
                        LectureRoom.objects.create(user=user, lecture=lecture)
                    
                    Dashboard.objects.create(user=user)
                    dashboard = Dashboard.objects.get(user_id = user_id)
                    for lecture_category in LectureCategory.objects.all().order_by('id'):
                        UserGrowths.objects.create(lecture_category=lecture_category, dashboard=dashboard)
                    for homework in Homework.objects.all().order_by('id'):
                        Submission.objects.create(dashboard=dashboard, homework=homework)
                    
                    user.last_login = timezone.now()
                    user.save()
                    login(user) 
                    return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)
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
                
                
@decorators.permission_classes([permissions.IsAuthenticated])
class LogoutView(APIView):
    def post(self, request):
        try:
            
            refreshToken = request.COOKIES.get('refresh')
            
            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
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
        print(req_key)
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