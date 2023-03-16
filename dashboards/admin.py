from django.contrib import admin
from .models import Dashboard, UserGrowth

@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):  
    list_display = ("id", "user","attendance", "homework_progress",)
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("id",)
    
@admin.register(UserGrowth)
class UserGrowthAdmin(admin.ModelAdmin):  
    list_display = ("id", "dashboard","lecture_category", "ability",)
    list_filter = ("dashboard","lecture_category", "ability",)
    ordering = ("id","dashboard",)
