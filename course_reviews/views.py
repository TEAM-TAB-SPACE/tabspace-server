from rest_framework import viewsets, exceptions, status
from rest_framework.response import Response
from rest_framework.views    import APIView
from .serializers import CourseReviewSerializer
from .models import CourseReview


class CourseReviewView(APIView):
    def post(self, request):
        user_id = 9
        data = request.data.copy()
        data['user'] = user_id
        serializer = CourseReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED,data=serializer.data)
        