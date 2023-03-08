from rest_framework import serializers
from .models import User



        
class KakaoSerializer(serializers.Serializer):
    code = serializers.CharField()  
    
class UserRegisterSerializer(serializers.ModelSerializer):
    # secret_key = UserSecretKeySerializer()
    class Meta:
        model = User
        exclude = ('password',)
        
class UserSerializer(serializers.ModelSerializer):
    # secret_key = UserSecretKeySerializer()
    class Meta:
        model = User
        fields = ('realname',)