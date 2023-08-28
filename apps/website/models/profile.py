from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    UserGender = [("Male", "Male"), ("Female", "Female")]

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile_user')
    phone = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=6, choices=UserGender, default="Male")
    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    # profile picture name
    profile_pic = models.CharField(max_length=255, null=True, blank=True)
