from rest_framework import serializers
from .models import CourseReview
from users.serializers import UserSerializer

class CourseReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseReview
        fields = '__all__'
        