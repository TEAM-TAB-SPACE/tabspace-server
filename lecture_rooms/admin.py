from django.contrib import admin
from .models import LectureRoom

@admin.register(LectureRoom)
class LectureAdmin(admin.ModelAdmin):  
    list_display = ("id", "user","lecture", "playtime","endtime", "progress", "completed", "is_clicked",)
    list_filter = ("user","lecture", "playtime","endtime", "progress", "completed", "is_clicked",)
    search_fields = ("user","lecture",)
    ordering = ("id",)
    
