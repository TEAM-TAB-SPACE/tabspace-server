from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/secretkeys/", include("secretkeys.urls")),   
    path("api/lectures/", include("lectures.urls")),   
    path("api/lecturerooms/", include("lecture_rooms.urls")),   
    path("api/homeworks/", include("homeworks.urls")),   
]
