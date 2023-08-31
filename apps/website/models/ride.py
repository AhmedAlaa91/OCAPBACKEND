from django.contrib.auth.models import User
from django.db import models

from .CarRegistration import Car


class Ride(models.Model):
    RIDE_TYPES = [
        ("To Office", "To Office"),
        ("From Office", "From Office"),
        ("2-Way Ride", "2-Way Ride"),
    ]

    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, choices=RIDE_TYPES, default="To Office")
    date = models.DateField()
    leave_time = models.TimeField()
    return_time = models.TimeField(null=True, blank=True)
    no_of_seats = models.IntegerField(default="3")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    restrictions = models.CharField(null=True, blank=True, max_length=100)
    meeting_point = models.CharField(null=True, blank=True, max_length=300)
    Car_Pallet_Number = models.CharField(max_length=50, blank=True)
    distance = models.IntegerField(null=True, blank=True)
