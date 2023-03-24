from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('refresh', views.CookieTokenRefreshView.as_view()),
    path("username", views.UserNameView.as_view()),
    path("register/validation", views.KakaoRegisterValidationView.as_view()),
    path('register',views.KakaoRegisterView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('admin/login', views.StaffLoginView.as_view()),
    
]