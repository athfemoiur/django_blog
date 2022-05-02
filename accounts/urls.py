from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, UserInfoView, UserInfoUpdateView, UserChangePasswordView

app_name = 'blog'

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('user-update/', UserInfoUpdateView.as_view(), name='user-update'),
    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),

]