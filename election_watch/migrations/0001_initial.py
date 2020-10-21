# Generated by Django 3.0.8 on 2020-10-13 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, null=True, unique=True)),
                ('email', models.EmailField(max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email_address')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('telephone', models.IntegerField()),
                ('city', models.CharField(blank=True, max_length=400, null=True)),
                ('address_line', models.CharField(blank=True, max_length=400, null=True)),
                ('street', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='lat')),
                ('lng', models.FloatField(blank=True, null=True, verbose_name='lng')),
                ('polling_station', models.CharField(db_index=True, max_length=100, unique=True)),
                ('address', models.CharField(blank=True, max_length=400, null=True)),
                ('city', models.CharField(blank=True, max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='election_watch.Admin')),
            ],
        ),
    ]
