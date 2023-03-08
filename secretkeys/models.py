from django.db import models
from common.models import CommonModel
from django.core.validators import RegexValidator


# 회원가입시 입력하는 이름과 폰번호가 사용하려는 secretkey 정보와 일치하여야 한다
class SecretKey(CommonModel):
    phoneNumberRegex = RegexValidator(regex = r'^010([0-9]{4})([0-9]{4})$', message='Enter a valid phone number.',code=400)
    
    master = models.CharField(max_length=50, unique=True, blank=False, null=False)
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)
    key = models.CharField(max_length=20, unique=True, blank=False, null=False)
    active = models.BooleanField(default=True, null=False)
    def __str__(self):
        return self.key