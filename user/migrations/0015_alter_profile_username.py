# Generated by Django 5.0.4 on 2024-06-04 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_profile_phone_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(default='username', max_length=50, null=None, unique=True),
        ),
    ]
