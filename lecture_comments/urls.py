from django.urls import path
from . import views

urlpatterns = [
    path('reviews', views.LectureCommentsView.as_view()),
    
]