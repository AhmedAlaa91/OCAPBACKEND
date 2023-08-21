from django.contrib.auth.models import User
from django.db import models
from .ride import Ride


class RidesBooked(models.Model):
    request_status = [
        ('1', 'Pending'),
        ('2', 'Accepted'),
        ('3', 'Rejected'),
        ('4', 'Cancelled')
    ]
    Requestor = models.ForeignKey(User, on_delete=models.CASCADE)
    RideRequested = models.ForeignKey(Ride, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=request_status, default='1')
    comment = models.CharField(max_length=50, null=True, blank=True)
