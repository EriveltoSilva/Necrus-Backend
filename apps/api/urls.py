from . import views
from rest_framework import routers
from django.urls import path, include
from apps.userauths import views as userauths_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('user/token/', userauths_views.MyTokenObtainPairView.as_view()),    
    path('user/token/refresh', TokenRefreshView.as_view()),    
    path('user/register/', userauths_views.RegisterView.as_view()),    
    path('user/password-reset/<str:email>/', userauths_views.PasswordResetEmailVerifyView.as_view()),    
    path('user/password-change/', userauths_views.PasswordChangeView.as_view(), name="password_change"),    
]