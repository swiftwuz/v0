from rest_framework.validators import UniqueValidator
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from .models import User, PollingAgent


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=55, min_length=8, write_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = "__all__"

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

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
        )
        PollingAgent.objects.create(user=user).save()

        password = validated_data["password"]
        user.set_password(password)

        user.is_pollingagent = True
        user.save()
        return user


class OTPVerification(serializers.ModelSerializer):
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



