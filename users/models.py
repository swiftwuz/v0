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

        user = self.model(
            phone_number=phone_number,
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email,
                         phone_number=None, password=None):

        if password is None:
            raise TypeError("Password cannot be empty.")
        if email is None:
            raise TypeError("Must provide email")

        phone_number = input("Phone Number: ")
        user = self.create_user(username, email, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


#  set all blank and null to False
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=100, unique=True, db_index=True)

    otp_confirmed = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$',
        message="Phone number must be entered in the format 0XXXXXXX")

    phone_number = models.CharField(validators=[phone_regex], max_length=15,
                                    blank=True, unique=True)

    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    affliation = models.CharField(max_length=100, null=True)
    affliation_code = models.IntegerField(blank=True, null=True)

    address = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    is_pollingagent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class PollingAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)

    email = models.EmailField(max_length=100, unique=True, db_index=True,
                              null=True)

    username = models.CharField(max_length=100, unique=True, db_index=True,
                                null=True)

    objects = UserManager()

    def __str_(self):
        return f"{self.user}"
