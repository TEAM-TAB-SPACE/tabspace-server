from rest_framework import exceptions, status, decorators, permissions
from rest_framework.response import Response
from rest_framework.views    import APIView
from .serializers import CourseReviewSerializer
from .models import CourseReview

@decorators.permission_classes([permissions.IsAuthenticated])
class CourseReviewView(APIView):
    def post(self, request):
        
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = CourseReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED,data=serializer.data)
    
@decorators.permission_classes([permissions.IsAuthenticated])
class AdminCourseReviewsView(APIView):
    def get(self, request):
        reviews=CourseReview.objects.all()
        serializer = CourseReviewSerializer(reviews, many=True)
        
        return Response(status=status.HTTP_200_OK,data=serializer.data)