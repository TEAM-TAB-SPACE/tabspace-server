from django.urls import path
from . import views

urlpatterns = [
    path('info', views.ApplierView.as_view()),
    path('admin/info', views.AdminApplierView.as_view())

]