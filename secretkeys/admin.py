from django.contrib import admin
from .models import SecretKey

@admin.register(SecretKey)
class SecretKeyAdmin(admin.ModelAdmin):  
    list_display = ("id", "master","phone", "key","active")
    list_filter = ("master","phone", "key","active")
    search_fields = ("master","phone", "key",)
    ordering = ("id",)

