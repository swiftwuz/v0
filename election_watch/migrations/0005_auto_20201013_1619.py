# Generated by Django 3.0.8 on 2020-10-13 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('election_watch', '0004_auto_20201013_1549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='password1',
            new_name='password',
        ),
    ]
