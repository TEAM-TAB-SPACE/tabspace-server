from django.urls import path
from . import views

urlpatterns = [
    path('dbCreate/', views.dbCreateView),
    path('dbUpdateActive/', views.dbUpdateActiveView),
    path('dbUpdateDate/', views.dbDateUpdateView),
    
]