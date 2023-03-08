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




class LectureRoomsView(APIView):
    def get(self, request):
        try:
            user_id = 5   #나중에 수정 
            lecture_rooms = LectureRoom.objects.filter(user=user_id)
            serializer = serializers.LectureRoomsSerializer(lecture_rooms, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except LectureRoom.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='This LecureRoom does not exist')
        
    def post(self, request):
        try:
            if not 'id' in request.data:
                raise exceptions.ParseError('error:"id" is required')
            if len(request.data)==1:
                raise exceptions.ParseError('error: there is no data to be updated')
            
            lecture_room = LectureRoom.objects.get(id=request.data['id'])
            if lecture_room.user_id != 5: #나중에 수정 
                raise exceptions.PermissionDenied('This user do not have permission of this lectureroom')
            serializer = serializers.LectureRoomSerializer(lecture_room, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(data=request.data, status=status.HTTP_206_PARTIAL_CONTENT)
        except LectureRoom.DoesNotExist:
            return Response(data='This lectureRoom does not exist', status=status.HTTP_404_NOT_FOUND)