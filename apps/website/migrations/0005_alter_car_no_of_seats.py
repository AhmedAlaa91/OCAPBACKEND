# Generated by Django 4.1.9 on 2023-07-04 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_alter_car_car_pallet_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="car",
            name="No_OF_Seats",
            field=models.IntegerField(default="3", max_length=10),
        ),
    ]