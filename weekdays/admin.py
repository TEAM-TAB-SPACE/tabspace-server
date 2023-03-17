from django.contrib import admin

from .models import Weekday

@admin.register(Weekday)
class DashboardAdmin(admin.ModelAdmin):  
    list_display = ("month", "days","korean_holidays", )
    
