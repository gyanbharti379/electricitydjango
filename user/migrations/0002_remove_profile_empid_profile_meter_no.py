# Generated by Django 5.0.4 on 2024-04-25 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='empid',
        ),
        migrations.AddField(
            model_name='profile',
            name='meter_no',
            field=models.IntegerField(default=None, max_length=10, unique=True),
        ),
    ]
