from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path("callback/kakao", views.KaKaoSignInCallBackView.as_view()),
    path("register/validation", views.KakaoRegisterValidationView.as_view()),
    path('register',views.KakaoRegisterView.as_view()),
    path('logout', views.LogoutView.as_view())
    
]