# Generated by Django 4.1.9 on 2023-09-01 12:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="car",
            name="Engine_size",
        ),
        migrations.RemoveField(
            model_name="car",
            name="Fuel_consumption",
        ),
        migrations.RemoveField(
            model_name="car",
            name="No_clyender",
        ),
    ]
