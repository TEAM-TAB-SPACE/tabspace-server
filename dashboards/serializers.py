from rest_framework import serializers
from .models import Dashboard,UserGrowth
from lectures.serializers import LectureCategorySerializer
from users.serializers import UserSerializer
from homeworks.serializers import AdminSubmissionSerializer

class UserGrowthsSerializer(serializers.ModelSerializer):
    
    lecture_category = LectureCategorySerializer()
    class Meta:
        model = UserGrowth
        fields = '__all__'
        
        
class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dashboard
        fields = ('attendance', )
        
class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dashboard
        fields = ('notifications', )
        
class AdminAttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Dashboard
        fields = ('user', 'attendance', )
        
class AdminHomeworkSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    submission = AdminSubmissionSerializer(many = True)
    class Meta:
        model = Dashboard
        fields = ('id','user', 'submission',)