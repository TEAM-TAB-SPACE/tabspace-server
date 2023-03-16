from django.urls import path
from . import views

urlpatterns = [
    path('dbCreate/', views.dbCreateView),
    path('submission',views.SubmissionView.as_view())
]