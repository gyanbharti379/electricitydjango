# Generated by Django 5.0.4 on 2024-06-11 06:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_reminder_meter_no_servicecharge_meter_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cus_last_login',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='meterinfo',
            name='date_of_reg',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cus_doj',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='reminder',
            name='reminder_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
