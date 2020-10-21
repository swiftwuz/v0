from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    RegisterView, VerifyEmail, LoginAPIView, VerifyPhone,
    PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPasswordAPIView,
    LogoutAPIView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('verify-email/', VerifyEmail.as_view(), name="verify-email"),

    path('verify-phone/', VerifyPhone.as_view(),
         name="verify-number"),

    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),

    path('token-check/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name="token-check"),

    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name="password-reset-complete"),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
