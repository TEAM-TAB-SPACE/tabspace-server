from rest_framework import serializers
from .models import LectureComment,CommentReply
from users.serializers import UserSerializer


        
class CommentReplySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = CommentReply
        fields = ('user','reply')
        
class LectureCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    replies = CommentReplySerializer(many=True)
    class Meta:
        model = LectureComment
        fields = ('user','comment','replies')