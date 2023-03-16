from rest_framework import serializers
from .models import Lecture, LectureCategory



        
class LectureCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LectureCategory
        fields = ('name',)
        
class LectureSerializer(serializers.ModelSerializer):
    category = LectureCategorySerializer()
    class Meta:
        model = Lecture
        fields = '__all__'
        
class DashboardLectureSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lecture
        fields = ('title', 'videoId')