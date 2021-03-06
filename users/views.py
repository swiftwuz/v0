import requests
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication
from django.urls import reverse
from django.conf import settings
import jwt
import pyotp

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str, smart_bytes, DjangoUnicodeDecodeError
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# from .signals import generate_key

from .serializers import (
    RegisterSerializer, EmailVerificationSerializer, LoginSerializer,
    OTPVerification, ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer, LogoutSerializer
)
from .models import User
from .utils import Util
from .renderers import UserRenderer

ark_phone = settings.ARK_PHONE
auth_token = settings.ARK_AUTH_TOKEN


def generate_key():
    global totp
    otp = pyotp.random_base32()
    totp = pyotp.TOTP(otp, interval=300)
    one_time = totp.now()
    print(one_time)
    return one_time


def verify_otp(password):
    result = totp.verify(password)
    return result


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        # user = User.objects.get(email=user_data['email'])

        # token = RefreshToken.for_user(user).access_token

        # current_site = get_current_site(request).domain
        # relative_link = reverse("verify-email")

        # absurl = "http://" + current_site + \
            # relative_link + "?token=" + str(token)

        # email_body = "Hi " + user.username + \
            # ", use link below to verify your email. " + absurl

        # data = {'email_body': email_body, "recipient": user.email,
                # "email_subject": "Verify your email."}
        # Util.send_email(data)

        otp = generate_key()
        user_number = request.data.get("phone_number")
        body = "Your verification code is " + otp[:7]

        payload = {
            "from": ark_phone,
            "to": user_number,
            "sms": body,
            "api_key": auth_token,
        }
        url = "https://sms.arkesel.com/sms/api?action=send-sms&api_key= \
            {auth_token}&to={user_number}&from={ark_phone}&sms={body}"
        requests.post(url, payload)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyPhone(views.APIView):
    serializer_class = OTPVerification

    def post(self, request):
        OTPVerification(data=request.data)
        phone_number = request.data["phone_number"]
        password = request.data["otp"]
        verify = verify_otp(password)
        if verify:
            User.objects.filter(phone_number=phone_number).update(
                is_verified=True, otp_confirmed=True
            )
            return Response("Phone Number verified successfully",
                            status=status.HTTP_201_CREATED)
        return Response("Verifiication code did not match. Please retry.",
                        status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {'msg': 'Account successfully activated.'},
                status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'msg': 'Activation link expired.'},
                            status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError:
            return Response({'msg': 'Invalid Activation.'},
                            status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        self.serializer_class(data=request.data)
        email = request.data["email"]
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain

            relative_link = reverse("password-reset-confirm",
                                    kwargs={
                                        "uidb64": uidb64,
                                        "token": token
                                    })

            absurl = "http://" + current_site + relative_link
            email_body = "Hello, use link below to reset your password. " \
                + absurl

            data = {'email_body': email_body, "recipient": user.email,
                    "email_subject": "Reset your password."}

            Util.send_email(data)

        return Response({"success": "Please check your mail for a password reset link."},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is invalid. \
                                 Please request a new one."},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({"success": True,
                             "message": "Valid credentials.",
                             "uidb64": uidb64,
                             "token": token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            return Response({"error": "Token is invalid. \
                             Please request a new one."},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True,
                         "message": "Password reset success."},
                        status=status.HTTP_200_OK)


class LoginAPIView(views.APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
