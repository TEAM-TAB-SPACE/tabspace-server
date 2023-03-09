from django.contrib import admin

from .models import Lecture

@admin.register(Lecture)
class UserAdmin(admin.ModelAdmin):  
    list_display = ("id", "title","category", "teacher","duration", "videoId", "date", "today_lecture", "active_lecture")
    list_filter = ("title","category", "teacher","duration", "videoId", "date", "today_lecture", "active_lecture")
    search_fields = ("title", )
    ordering = ("id",)
