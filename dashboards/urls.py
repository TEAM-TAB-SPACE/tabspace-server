from django.urls import path
from . import views

urlpatterns = [
    path('todaylectures',views.TodayLectureView.as_view()),
    path('usergrowths',views.UserGrowthView.as_view()),
    path('latest',views.LatestVideoView.as_view()),

]