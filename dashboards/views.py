from django.shortcuts import render
from . import serializers
import pandas as pd
import random
from django.http import HttpResponse, Http404
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from datetime import datetime
import requests
from dateutil.relativedelta import *
from lectures.models import Lecture
from lectures.serializers import DashboardLectureSerializer
from lecture_rooms.models import LectureRoom
from lecture_rooms.serializers import DashboardLectureRoomSerializer
from .models import UserGrowth, Dashboard
from .serializers import AttendanceSerializer, AdminAttendanceSerializer, AdminHomeworkSerializer, NotificationSerializer

@decorators.permission_classes([permissions.IsAuthenticated])
class TodayLectureView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            today_lectures = Lecture.objects.filter(today_lecture=1)
            lecture_rooms = LectureRoom.objects.filter(user_id=user_id, lecture__in =today_lectures)
            
            serializer = DashboardLectureRoomSerializer(lecture_rooms, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Lecture.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='holiday')
            
@decorators.permission_classes([permissions.IsAuthenticated])
class UserGrowthView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            dashboard = Dashboard.objects.get(user_id=user_id)
            print(dashboard)
            growths = UserGrowth.objects.filter(dashboard= dashboard)
            print(growths)
            serializer = serializers.UserGrowthsSerializer(growths, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Dashboard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='this dashboard does not exist')

@decorators.permission_classes([permissions.IsAuthenticated])
class LatestVideoView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            lecture_room = LectureRoom.objects.filter(user_id=user_id)
            latest_lecture = lecture_room.latest('updated_at')
            if latest_lecture.playtime==0:
                return Response(status=status.HTTP_204_NO_CONTENT, data='수강한 강의가 없음')
            latest_lecture = latest_lecture.lecture
            print(latest_lecture)            
           
            serializer= DashboardLectureSerializer(latest_lecture)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except LectureRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='this lectureroom does not exist')

@decorators.permission_classes([permissions.IsAuthenticated])       
class AttendanceView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            dashboard = Dashboard.objects.get(user_id=user_id)          
            serializer= AttendanceSerializer(dashboard)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Dashboard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='this dashboard does not exist')

@decorators.permission_classes([permissions.IsAuthenticated])
class NotificationView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            dashboard = Dashboard.objects.get(user_id=user_id)          
            serializer= NotificationSerializer(dashboard)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Dashboard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='this dashboard does not exist')              


### admin page views
@decorators.permission_classes([permissions.IsAuthenticated])
class AdminAttendanceView(APIView):
    def get(self, request):
        try:
            dashboard = Dashboard.objects.all()        
            serializer= AdminAttendanceSerializer(dashboard, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Dashboard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='dashboard does not exist')
        
@decorators.permission_classes([permissions.IsAuthenticated])
class AdminHomeworkView(APIView):
    def get(self, request):
        try:
            dashboard = Dashboard.objects.all() 
            serializer= AdminHomeworkSerializer(dashboard, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Dashboard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='dashboard does not exist')
        
        
