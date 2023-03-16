from rest_framework import serializers
from .models import Homework, Submission

class HomeworkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Homework
        fields = ('title',)

class SubmissionSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer()
    class Meta:
        model = Submission
        fields = '__all__'
        