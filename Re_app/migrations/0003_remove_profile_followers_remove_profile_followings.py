# Generated by Django 4.0 on 2022-05-18 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Re_app', '0002_alter_profile_followers_alter_profile_followings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='followings',
        ),
    ]
