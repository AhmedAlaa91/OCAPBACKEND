from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from .profile import Profile


class Car(models.Model):
    CarReg_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False,
    )
    No_OF_Seats = models.IntegerField(max_length=10)
    Car_Pallet_Number = models.IntegerField(max_length=10)
    Car_Manufacture = models.CharField(max_length=50)
    Car_Color = models.CharField(max_length=50)
    Owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
    )
