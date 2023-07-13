from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    UserGender = [('Male', 'Male'), ('Female', 'Female')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=6, choices=UserGender, default='Male')
    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        app_label = "website"
