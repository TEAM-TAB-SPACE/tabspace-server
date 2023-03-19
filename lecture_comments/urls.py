from django.urls import path
from . import views

urlpatterns = [
    path('reviews', views.LectureCommentsView.as_view()),
    path('review', views.LectureCommentView.as_view()),
    path('reply', views.CommentReplyView.as_view()),
    
]