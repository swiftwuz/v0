from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class UserManager(BaseUserManager):

    def create_user(self, username, email, phone_number, password=None):
        if username is None:
            raise TypeError("Must provide username.")

        if email is None:
            raise TypeError("Must provide email.")

        if phone_number is None:
            raise TypeError("Must provide phone_number.")

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, phone_number, password=None):
        if password is None:
            raise TypeError("Password cannot be empty.")
        if email is None:
            raise TypeError("Must provide email")
        if phone_number is None:
            raise TypeError("Phone number cannot be empty.")

        user = self.create_user(username, email, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)

    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$',
        message="Phone number must be entered in the format 0XXXXXXX")

    phone_number = models.CharField(validators=[phone_regex], max_length=15,
                                    blank=True, unique=True)

    is_staff = models.BooleanField(default=False)
    is_pollingagent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email_subject}"

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class PollingAgentManager(BaseUserManager):

    def create_user(self, username, email, phone_number, password=None):
        if username is None:
            raise TypeError("Must provide username.")

        if email is None:
            raise TypeError("Must provide email.")

        if phone_number is None:
            raise TypeError("Must provide phone_number.")

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class PollingAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    password = models.CharField(max_length=128, verbose_name="password", null=True)

    otp_confirmed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    affliation = models.CharField(max_length=100)
    affliation_code = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=20)
    country = models.CharField(max_length=20)

    objects = PollingAgentManager()

    def __str_(self):
        return f"{self.first_name} + {self.last_name} \
    is affliated to {self.affliation}."
