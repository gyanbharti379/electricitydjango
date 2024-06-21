# Generated by Django 5.0.4 on 2024-04-28 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_bill_reminder_meterinfo_status_profile_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='meter_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='total_bills',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bill',
            name='units',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='meterinfo',
            name='meter_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='meter_no',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicecharge',
            name='adv_deposite',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicecharge',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicecharge',
            name='con_charge',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicecharge',
            name='labour_charge',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicecharge',
            name='meter_charge',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='servicecharge',
            name='meter_file_charge',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tax',
            name='cost_per_unit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tax',
            name='fixed_tax',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tax',
            name='meter_rent',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tax',
            name='service_charge',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tax',
            name='service_tax',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tax',
            name='swacch_bharat_cess',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_profile_img',
            field=models.ImageField(default='media\\icon\\person-man.webp', upload_to='profile_img'),
        ),
    ]
