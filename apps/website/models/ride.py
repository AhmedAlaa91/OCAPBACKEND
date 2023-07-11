from django.contrib.auth.models import User
from django.db import models
from .CarRegistration import Car

class Ride(models.Model):
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    no_of_seats = models.IntegerField(default='3')
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    restrictions = models.CharField(blank=True, max_length=100)

    class Meta:
        app_label = "website"

