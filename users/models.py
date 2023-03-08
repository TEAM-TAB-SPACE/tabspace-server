from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    phoneNumberRegex = RegexValidator(regex = r'^010([0-9]{4})([0-9]{4})$', message='Enter a valid phone number.',code=400)
    
    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    realname = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)
    email = models.EmailField(blank=False, null=False, unique = True)
    msg_agree = models.BooleanField(default=False, blank=True, null=False)
    secret_key = models.CharField(max_length=20, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.username
