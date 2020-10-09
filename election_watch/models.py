from django.db import models
from PIL import Image
from django.contrib.auth.models import (
    BaseUserManager
)
from users.models import User


class AdminManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError("Must provide username.")

        if email is None:
            raise TypeError("Must provide email.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                parent_link=True, default=True,
                                primary_key=True)

    username = models.CharField(max_length=100, unique=True, null=True)
    email = models.EmailField(max_length=100, unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']

    objects = AdminManager()

    def __str__(self):
        return f"{self.email}"


class Profile(models.Model):
    admin = models.OneToOneField(Admin, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_image(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    lat = models.FloatField('lat', blank=True, null=True)
    lng = models.FloatField('lng', blank=True, null=True)

    polling_station = models.CharField(max_length=100,
                                       unique=True, db_index=True)

    address = models.CharField(max_length=400, blank=True, null=True)
    city = models.CharField(max_length=400, blank=True, null=True)


class Institution(models.Model):
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100, unique=True, db_index=True)
    telephone = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=400, blank=True, null=True)
    address_line = models.CharField(max_length=400, blank=True, null=True)
    street = models.CharField(max_length=400, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
