from rest_framework import serializers
from .models import User



        
class KakaoSerializer(serializers.Serializer):
    code = serializers.CharField()  
    
class UserRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ('password',)
class UserRegisterValidationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        exclude = ('password','username')
        
class UserIdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','realname',)
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('realname',)
        
class StaffloginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username','password',)