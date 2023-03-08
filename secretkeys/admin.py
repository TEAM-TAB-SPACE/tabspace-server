from django.contrib import admin
from .models import SecretKey

@admin.register(SecretKey)
class SecretKeyAdmin(admin.ModelAdmin):  
    pass