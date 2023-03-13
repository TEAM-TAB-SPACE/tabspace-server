from django.shortcuts import render
import pandas as pd
import random
from .models import Homework
from django.http import HttpResponse, Http404
from rest_framework.views    import APIView
from rest_framework.response import Response
from rest_framework import exceptions, decorators, permissions, status
from datetime import datetime
import requests
from dateutil.relativedelta import *
# from . import serializers 


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
