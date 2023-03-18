from django.db import models
from common.models import CommonModel
from django.core.validators import RegexValidator


class Applier(CommonModel):
    phoneNumberRegex = RegexValidator(regex = r'^010([0-9]{4})([0-9]{4})$', message='Enter a valid phone number.',code=400)
    categorys = (
    	('U', 'U'),
        ('F', 'F'),
        ('B', 'B'),
    )
    
    
    
    category = models.CharField(max_length=1, blank=False, null=False, choices=categorys)
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 11, unique = True)

    def __str__(self):
        return self.phone

