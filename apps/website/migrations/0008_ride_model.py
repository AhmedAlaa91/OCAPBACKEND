from django.db import migrations, models
import django.db.models.deletion
from datetime import datetime

class Migration(migrations.Migration):
    dependencies = [
        ("website", "0007_alter_carplate_letter_one"),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('city', models.CharField(max_length=50)),
                ('area', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50, choices=[('To Office', 'To Office'), ('From Office', 'From Office'), ('2-Way Ride', '2-Way Ride')], default='To Office')),
                ('date', models.DateField()),
                ('leave_time', models.TimeField()),
                ('return_time', models.TimeField(null=True, blank=True)),
                ('no_of_seats', models.IntegerField(default='3')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.car')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('restrictions', models.CharField(null=True, blank=True, max_length=100)),
                ('meeting_point', models.CharField(null=True, blank=True, max_length=300)),

            ],
        ),
    ]
