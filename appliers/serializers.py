from rest_framework import serializers
from .models import Applier


class ApplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Applier
        fields = '__all__'