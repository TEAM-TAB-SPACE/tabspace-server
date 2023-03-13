from django.contrib import admin

from .models import Homework, Submission

@admin.register(Homework)
class UserAdmin(admin.ModelAdmin):  
    pass

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):  
    pass

