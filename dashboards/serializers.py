from rest_framework import serializers
from .models import Dashboard,UserGrowth
from lectures.serializers import LectureCategorySerializer


class UserGrowthsSerializer(serializers.ModelSerializer):
    
    lecture_category = LectureCategorySerializer()
    class Meta:
        model = UserGrowth
        fields = '__all__'