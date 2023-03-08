from django.urls import path
from . import views


urlpatterns = [
    path('', views.LectureRoomsView.as_view()),
    
    
]
