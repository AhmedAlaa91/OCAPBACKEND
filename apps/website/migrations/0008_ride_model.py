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
                ('source', models.CharField(max_length=50)),
                ('destination', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField()),
                ('return_date', models.CharField(max_length=50, blank=True)),
                ('no_of_seats', models.IntegerField(default='3')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.car')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('restrictions', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
