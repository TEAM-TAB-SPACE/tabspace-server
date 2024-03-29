from django.shortcuts import render
from . import serializers
import pandas as pd
import random
from .models import LectureRoom
from django.http import HttpResponse, Http404
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from datetime import datetime
import requests
from dateutil.relativedelta import *
from dashboards.models import Dashboard, UserGrowth
from lectures.models import Lecture
from django.core.cache import cache


           
import time
@decorators.permission_classes([permissions.IsAuthenticated])
class LectureRoomsView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            # user_id = 27
             
            lecture_rooms = LectureRoom.objects.filter(user=user_id)
            serializer = serializers.LectureRoomsSerializer(lecture_rooms, many=True)
             
            return Response(status=status.HTTP_200_OK,data=serializer.data)
           
        except LectureRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='This LecureRoom does not exist')
        
    def post(self, request):
        try:
            user_id = request.user.id
            if not 'id' in request.data:
                raise exceptions.ParseError('error:"id" is required')
            if len(request.data)==1:
                raise exceptions.ParseError('error: there is no data to be updated')
            
            lecture_room = LectureRoom.objects.get(id=request.data['id'])
            if lecture_room.completed == 1: #이미 다 들은 강의라면 endpoint 만 업데이트 한다.
                serializer = serializers.CompletedLectureRoomSerializer(lecture_room, data = request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
                
            if lecture_room.user_id != user_id:  
                raise exceptions.PermissionDenied('This user do not have permission of this lectureroom')
            copy_data = request.data.copy()
            
            if ('playtime' in request.data) and ('endtime' in request.data):
                difference = copy_data['endtime'] - lecture_room.endtime
                if copy_data['playtime'] > 0 and difference > 0:            #기존 endpoint 와 비교
                    copy_data['playtime'] += lecture_room.playtime         
                else:
                    copy_data['playtime'] = lecture_room.playtime                      #그렇지 않으면 그대로
                copy_data['endtime'] = copy_data['playtime']
            elif ('playtime' in request.data) or ('endtime' in request.data):
                raise exceptions.ParseError('error: both endtime and playtime needed')     
                                    
            serializer = serializers.LectureRoomSerializer(lecture_room, data=copy_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            lecture_duration = lecture_room.lecture.duration  
            import math          
            lecture_room.progress = math.ceil(lecture_room.playtime/lecture_duration*100)  
            lecture_room.save() 
            if lecture_room.progress >= 100:
                lecture_room.progress = 100   #progress 는 100을 넘지 않는다.
                lecture_room.save()
                if lecture_room.endtime >= lecture_duration-1:  #progress 는 100이고 endtime이 끝지점일 때만 강의 수강이 완료됨 (오차범위 1초)
                    lecture_room.completed = 1
                    lecture_room.save()
                    dashboard = Dashboard.objects.get(user_id=user_id)
                    lecture_category=lecture_room.lecture.category
                    user_growths = UserGrowth.objects.get(dashboard=dashboard, lecture_category= lecture_category)
                    user_growths.ability += math.ceil(100/len(Lecture.objects.filter(category = lecture_category)))
                    user_growths.save()
            return Response(data={'endtime':lecture_room.endtime,'playtime':lecture_room.playtime,'completed':lecture_room.completed, 'progress':lecture_room.progress,'is_clicked':lecture_room.is_clicked}, status=status.HTTP_206_PARTIAL_CONTENT)
        except LectureRoom.DoesNotExist:
            return Response(data='This lectureRoom does not exist', status=status.HTTP_404_NOT_FOUND)