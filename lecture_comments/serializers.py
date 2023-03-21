from rest_framework import serializers
from .models import LectureComment,CommentReply
from users.serializers import UserIdSerializer
from django.db import models

        
class CommentRepliesSerializer(serializers.ModelSerializer):
    user = UserIdSerializer()
    
    class Meta:
        model = CommentReply
        fields = ('id','user','comment')
        
class LectureCommentReplySerializer(serializers.ModelSerializer):
    user = UserIdSerializer()
    replies = CommentRepliesSerializer(many=True)
    
    class Meta:
        model = LectureComment
        fields = ('id','user','comment','replies')
        
class LectureCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureComment
        fields = '__all__'

class CommentReplySerializer(serializers.ModelSerializer):    
    
    class Meta:
        model = CommentReply
        fields = '__all__'