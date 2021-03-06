# Generated by Django 3.0.8 on 2020-10-13 15:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=100, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=100, unique=True)),
                ('otp_confirmed', models.BooleanField(default=False)),
                ('is_verified', models.BooleanField(default=False)),
                ('phone_number', models.CharField(blank=True, max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format 0XXXXXXX', regex='^(\\+\\d{1,2}\\s?)?1?\\-?\\.?\\s?\\(?\\d{3}\\)?[\\s.-]?\\d{3}[\\s.-]?\\d{4}$')])),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('affliation', models.CharField(max_length=100, null=True)),
                ('affliation_code', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=20, null=True)),
                ('is_pollingagent', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PollingAgent',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('email', models.EmailField(db_index=True, max_length=100, null=True, unique=True)),
                ('username', models.CharField(db_index=True, max_length=100, null=True, unique=True)),
            ],
        ),
    ]
