from rest_framework import serializers
from .models import LectureRoom
from lectures.serializers import LectureSerializer, DashboardLectureSerializer


class LectureRoomsSerializer(serializers.ModelSerializer):
    
    lecture = LectureSerializer()
    class Meta:
        model = LectureRoom
        exclude = ('user',)
        
class LectureRoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LectureRoom
        fields = ('playtime','endtime','is_clicked',)       
        
class CompletedLectureRoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LectureRoom
        fields = ('endtime',)
        
class DashboardLectureRoomSerializer(serializers.ModelSerializer):
    lecture = DashboardLectureSerializer()
    class Meta:
        model = LectureRoom
        fields = ('lecture','progress','completed',)