from django.urls import path
from . import views


urlpatterns = [
    path('room', views.LectureRoomsView.as_view()),
    
    
]
