# Generated by Django 4.1.9 on 2023-08-29 07:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0009_alter_profile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="car",
            name="Car_license",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="car",
            name="Driver_license",
            field=models.BooleanField(default=False),
        ),
    ]
