from rest_framework import serializers
from .models import SecretKey

class UserSecretKeySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SecretKey
        fields = ('key',)