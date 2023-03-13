from django.urls import path
from . import views

urlpatterns = [
    path('dbCreate/', views.dbCreateView),
    path('dbUpdate/', views.dbUpdateView),
    path('dbUpdateActive/', views.dbUpdateActiveView),
    path('dbUpdateDate/', views.dbDateUpdateView),
    
]