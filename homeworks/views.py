from django.shortcuts import render
import pandas as pd
import random
from .models import Homework, Submission, Storage
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
from users.models import User


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
            user_id = 9  
            if not 'id' in request.data:
                raise exceptions.ParseError('error:"id" is required')   #submission id
            if len(request.data)==1:
                raise exceptions.ParseError('error: there is no data to be updated')
            print(request.data['file'])
            if request.data['file'] == '':
                raise exceptions.ParseError('error: there is no data to be updated')
            
            submission = Submission.objects.get(id=request.data['id'])
            dashboard_id = submission.dashboard_id
            # user_id = Dashboard.objects.get(id=dashboard_id).user_id           
            user_uuid = User.objects.get(id=user_id).uuid
            # if user_id != 9: #나중에 수정 
            #     raise exceptions.PermissionDenied('This user do not have permission of this submission')
            file_serializer = serializers.StorageFileSerializer(submission, request.data, partial=True)
            file_serializer.is_valid(raise_exception=True)            
            
            s3 = boto3.client('s3')            
            now = datetime.now()
            now = now.strftime('%Y%m%d_%H%M%S')
            s3.upload_fileobj(file_serializer.validated_data['file'], settings.AWS_STORAGE_BUCKET_NAME, f'{user_uuid}/{submission.id}/{now}_'+file_serializer.validated_data['file'].name)
           
            s3_url = f"{settings.CLOUDFRONT}/{user_uuid}/{submission.id}/{now}_{file_serializer.validated_data['file'].name}"
            
            
            Storage.objects.create(submission = submission, url = s3_url)
            
            if submission.is_submitted == False:
                submission.is_submitted = True
                submission.save()
            return Response(status=status.HTTP_201_CREATED, data="homework submitted successfully")
        except Submission.DoesNotExist:
            return Response(data='This submission does not exist', status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        try:
            if not 'id' in request.data:
                raise exceptions.ParseError('error:"id" is required') #storageId
            else:
                storage = Storage.objects.get(id=request.data["id"])
                storage_file_name = "/".join(storage.url.split('/')[-3:])
                print(storage_file_name)
                s3 = boto3.client('s3')            
                s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=storage_file_name)
                storage.delete()
                try:
                    Storage.objects.get(submission=storage.submission_id)
                except Storage.DoesNotExist:
                    submission = Submission.objects.get(id=storage.submission_id) 
                    submission.is_submitted = 0
                    submission.save()  
                return Response(data='storage deleted', status=status.HTTP_200_OK)
        except Storage.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this storage dose not exist')

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
