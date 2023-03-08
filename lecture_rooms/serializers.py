from rest_framework import serializers
from .models import LectureRoom
from lectures.serializers import LectureSerializer


class LectureRoomsSerializer(serializers.ModelSerializer):
    
    lecture = LectureSerializer()
    class Meta:
        model = LectureRoom
        exclude = ('user',)
        
class LectureRoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LectureRoom
        fields = ('playtime','is_clicked','completed')
        
        