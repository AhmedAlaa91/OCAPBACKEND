# Generated by Django 4.1.9 on 2023-08-29 08:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0010_car_car_license_car_driver_license"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="Car_license",
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name="car",
            name="Driver_license",
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
