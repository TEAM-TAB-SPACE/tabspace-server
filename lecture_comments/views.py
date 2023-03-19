from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views    import APIView
from .serializers import LectureCommentReplySerializer, LectureCommentSerializer, CommentReplySerializer
from .models import LectureComment, CommentReply
from lecture_rooms.models import LectureRoom


class LectureCommentsView(APIView):
    def get(self, request):
        try:
            if not 'id' in request.data: #lecture_room_id
                raise exceptions.ParseError('error:"id" is required')
            
            lectureroom_id = request.data["id"]
            lecture_id=LectureRoom.objects.get(id=lectureroom_id).lecture_id
            comments = LectureComment.objects.filter(lecture_id=lecture_id)
            
            serializer = LectureCommentReplySerializer(comments, many=True)
            
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except LectureComment.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT,data='no comments')
      
class LectureCommentView(APIView):  
    def post(self, request):
        user_id = 9
        if not 'id' in request.data:  #lecture_room_id
            raise exceptions.ParseError('error:"id" is required') 
        lectureroom_id = request.data["id"]
        lecture_id=LectureRoom.objects.get(id=lectureroom_id).lecture_id
        data = request.data.copy()
        data["user"] = user_id
        data["lecture"] = lecture_id
        serializer = LectureCommentSerializer(data=data)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)              
        
    def put(self,request):
        try:        
            user_id = 9
            if (not 'id' in request.data) or (not 'comment' in request.data):  #comment_id
                raise exceptions.ParseError('error:"id" and "comment" are required')
            comment_id = request.data['id']
            comment = LectureComment.objects.get(id=comment_id, user=user_id) 
            serializer = LectureCommentSerializer(comment, request.data, partial=True)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data) 
        except LectureComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this lecture comment does not exist')            

    def delete(self,request):
        try:
            user_id = 9
            if not 'id' in request.data:  #comment_id
                raise exceptions.ParseError('error:"id" is required')
            comment_id = request.data['id']
            comment = LectureComment.objects.get(id=comment_id, user=user_id)
            comment.delete()
            return Response(status=status.HTTP_200_OK, data='deleted') 
        except LectureComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this lecture comment does not exist') 
                         

class CommentReplyView(APIView):  
    def post(self, request):
        user_id = 9
        data = request.data.copy()
        data["user"] = user_id
        serializer = CommentReplySerializer(data=data)
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=serializer.data) 
    def put(self,request):
        try:        
            user_id = 9
            if (not 'id' in request.data) or (not 'reply' in request.data):  #reply_id
                raise exceptions.ParseError('error:"id" and "reply" are required')
            reply_id = request.data['id']
            reply = CommentReply.objects.get(id=reply_id, user=user_id) 
            serializer = CommentReplySerializer(reply, request.data, partial=True)
            serializer.is_valid(raise_exception=True) 
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data) 
        except CommentReply.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this reply does not exist')   
    def delete(self,request):
        try:
            user_id = 9
            if not 'id' in request.data:  #reply_id
                raise exceptions.ParseError('error:"id" is required')
            reply_id = request.data['id']
            reply = LectureComment.objects.get(id=reply_id, user=user_id)
            reply.delete()
            return Response(status=status.HTTP_200_OK, data='deleted') 
        except LectureComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data='this reply does not exist') 
        
