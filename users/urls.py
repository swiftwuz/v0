from django.urls import path

from users.views import (
    RegisterView, VerifyEmail, LoginAPIView, LogOutView, VerifyPhone
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogOutView.as_view(), name="logout"),
    path('verify-email/', VerifyEmail.as_view(), name="verify-email"),

    path('verify-phone/', VerifyPhone.as_view(),
         name="verify-number"),
]
