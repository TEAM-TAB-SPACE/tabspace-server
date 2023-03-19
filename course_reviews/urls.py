from django.urls import path
from . import views

urlpatterns = [
    path('review', views.CourseReviewView.as_view()),
    path('admin/reviews', views.AdminCourseReviewsView.as_view())

]