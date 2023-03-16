from django.shortcuts import render
import pandas as pd
import random
from .models import Homework, Submission
from django.http import HttpResponse, Http404
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from datetime import datetime
import requests
from dateutil.relativedelta import *
from . import serializers
from dashboards.models import Dashboard
import boto3
from config import settings


class SubmissionView(APIView):
    def get(self, request):
        try:
            user_id = 9   #나중에 수정 
            dashboard_id = Dashboard.objects.get(user_id=user_id).id
            submission = Submission.objects.filter(dashboard_id=dashboard_id)
            serializer = serializers.SubmissionSerializer(submission, many=True)
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except Submission.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data='This submission does not exist')
        
    def post(self, request):
        try:
            if not 'id' in request.data:
                raise exceptions.ParseError('error:"id" is required')
            if len(request.data)==1:
                raise exceptions.ParseError('error: there is no data to be updated')
            
            submission = Submission.objects.get(id=request.data['id'])
            dashboard_id = submission.dashboard_id
            user_id = Dashboard.objects.get(id=dashboard_id).user_id
            if user_id != 9: #나중에 수정 
                raise exceptions.PermissionDenied('This user do not have permission of this submission')
            serializer = serializers.SubmissionSerializer(submission, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            s3 = boto3.client('s3')
            file = serializer.validated_data['file']
            s3.upload_file(f'{request.data["file"]}',
                   settings.AWS_STORAGE_BUCKET_NAME,
                   f'{user_id}/{file}')
            serializer.save()
            
            return Response(data=request.data, status=status.HTTP_206_PARTIAL_CONTENT)
        except Submission.DoesNotExist:
            return Response(data='This submission does not exist', status=status.HTTP_404_NOT_FOUND)


"""
db값 추가
"""
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import os
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRET_BASE_FILE = os.path.join(BASE_DIR, 'homeworks.csv')

def dbCreateView(request):

    db = pd.read_csv(SECRET_BASE_FILE, encoding='cp949')

    for i in range(0,len(db)):
        title = db['title'][i]
                     
        
        Homework.objects.create(title=title)
    return HttpResponse('새로운 data가 저장되었습니다')  
