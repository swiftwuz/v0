from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    force_str,
)
from django.utils.http import urlsafe_base64_decode
from .models import User, PollingAgent


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=55, min_length=8, write_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["email", "username", "password", "phone_number",
                  "first_name", "last_name", "affliation", "affliation_code",
                  "address", "country"]

    def validate(self, attrs):
        username = attrs.get("username", "")
        phone_number = attrs.get("phone_number", "")
        password = attrs.get("password", "")

        if not username.isalnum():
            raise serializers.ValidationError(
                "The username should only contain alphanumeric characters."
            )

        if not phone_number:
            raise serializers.ValidationError(
                "Phone number field cannot be empty."
            )

        if password.isdigit():
            return serializers.ValidationError(
                "Password must not contain only digits."
            )

        return attrs

    #  Add PollingAgent.objects.create(username=username, email=email)
    def create(self, validated_data):
        user = User.objects.create(
            **validated_data,
        )
        PollingAgent.objects.create(user=user).save()
        password = validated_data["password"]
        user.set_password(password)

        user.is_pollingagent = True
        user.save()
        return user


class OTPVerification(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=15)

    class Meta:
        fields = ["otp", "phone_number"]


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=55, min_length=3)
    password = serializers.CharField(
        max_length=55, min_length=8, write_only=True)

    username = serializers.CharField(max_length=55, min_length=8,
                                     read_only=True)
    token = serializers.CharField(max_length=555,
                                  read_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "token", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(
                "Invalid credentials. Please try again."
            )

        if not user.is_active:
            raise AuthenticationFailed(
                "Account must be disabled, please contact admin."
            )

        if not user.is_verified:
            raise AuthenticationFailed(
                "Email not verified. Please check your mail."
            )

        return {
            "email": user.email,
            "username": user.username,
            "token": user.token
        }


class ResetPasswordEmailRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=55, min_length=3)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,
                                     max_length=68, write_only=True)

    token = serializers.CharField(min_length=6,
                                  max_length=68, write_only=True)

    uidb64 = serializers.CharField(min_length=2,
                                   max_length=68, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid.", 401)

            user.set_password(password)
            user.save()

        except Exception:
            raise AuthenticationFailed("The reset link is invalid.", 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    error_message = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
