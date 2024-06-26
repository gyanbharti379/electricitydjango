# Generated by Django 5.0.4 on 2024-06-06 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_profile_remove_customer_address_remove_customer_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='reminder',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('cus_username', models.CharField(max_length=50, unique=True)),
                ('phoneno', models.CharField(max_length=50, unique=True)),
                ('message', models.CharField(max_length=100)),
                ('reminder_date', models.DateTimeField(default='')),
                ('status', models.CharField(default='pending', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='cus_last_login',
            field=models.DateTimeField(default=''),
        ),
        migrations.AddField(
            model_name='meterinfo',
            name='date_of_reg',
            field=models.DateTimeField(default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='cus_doj',
            field=models.DateTimeField(default=''),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='abc@gmail.com', max_length=254),
        ),
    ]
