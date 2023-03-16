from django.urls import path
from . import views

urlpatterns = [
    path('review', views.CoursereviewViewSet.as_view())

]