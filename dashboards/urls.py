from django.urls import path
from . import views

urlpatterns = [
    path('todaylectures',views.TodayLectureView.as_view()),
    path('usergrowths',views.UserGrowthView.as_view()),
    path('latest',views.LatestVideoView.as_view()),
    path('attendance',views.AttendanceView.as_view()),
    path('notification',views.NotificationView.as_view()),
    
    path('admin/attendances',views.AdminAttendanceView.as_view()),
    path('admin/homeworks',views.AdminHomeworkView.as_view()),   
]