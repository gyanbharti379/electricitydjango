# Generated by Django 5.0.4 on 2024-06-04 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_no',
            field=models.CharField(default='111111111', max_length=50, unique=True),
        ),
    ]