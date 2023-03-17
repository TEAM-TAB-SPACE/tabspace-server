from rest_framework import serializers
from .models import Homework, Submission, Storage


        
class StorageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Storage
        fields = ('id','url', )
                
class StorageFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Storage
        fields = ('file',)
        
class HomeworkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Homework
        fields = ('title',)


class SubmissionSerializer(serializers.ModelSerializer):
    homework = HomeworkSerializer()
    storages = StorageSerializer(many = True)
    class Meta:
        model = Submission
        fields = ('id', 'homework', 'is_submitted', 'storages')
        

        