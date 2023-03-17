from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/secretkeys/", include("secretkeys.urls")),   
    path("api/lectures/", include("lectures.urls")),   
    path("api/lecturerooms/", include("lecture_rooms.urls")),   
    path("api/homeworks/", include("homeworks.urls")),   
    path("api/dashboards/", include("dashboards.urls")),   
    path("api/course/", include("course_reviews.urls")),   
    path("api/comment/", include("lecture_comments.urls")),   
    path("api/weekdays/", include("weekdays.urls")),   
]
