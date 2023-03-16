from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views    import APIView
from .serializers import LectureCommentSerializer, CommentReplySerializer
from .models import LectureComment, CommentReply



class LectureCommentView(APIView):
    def get(self, request):
        try:
            if not 'lecture_id' in request.data:
                raise exceptions.ParseError('error:"lecture_id" is required')
            print(request.data)
            comments = LectureComment.objects.filter(lecture_id=request.data['lecture_id'])
            
            serializer = LectureCommentSerializer(comments, many=True)
            
            return Response(status=status.HTTP_200_OK,data=serializer.data)
        except LectureComment.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT,data='no comments')
        
    # def post(self, request):
    #     user_id = 9
    #     data = request.data.copy()
    #     data['user'] = user_id
    #     serializer = CourseReviewSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        
