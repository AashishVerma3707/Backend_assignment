# Generated by Django 4.0 on 2022-05-18 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Re_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.IntegerField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='followings',
            field=models.IntegerField(max_length=5, null=True),
        ),
    ]
