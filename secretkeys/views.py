from django.shortcuts import render
import pandas as pd
import random
from .models import SecretKey
from django.http import HttpResponse, Http404
from rest_framework.views    import APIView
from . import serializers
from rest_framework.response import Response


    
"""
db값 추가
"""

def dbsaveView(request):
    master_list = ['관리자', '박찬양', '김미성', '문예림', '이다경', '이은빈']
    phone_list = ['01000000000', '01096244289', '01099441571','01074880222','01075121479','01086039174']
    
    for i in range(0,6):
        master = master_list[i]
        phone = phone_list[i]
        key = str(i)*4
        print(master,phone,key)
        SecretKey.objects.create(master=master, phone=phone, key=key, active=1)
    return HttpResponse('새로운 data가 저장되었습니다')