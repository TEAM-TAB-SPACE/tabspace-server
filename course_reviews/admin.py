from django.contrib import admin
from .models import CourseReview
# Register your models here.
@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):  
    list_display = ("id", "user","score", "comment",)
   