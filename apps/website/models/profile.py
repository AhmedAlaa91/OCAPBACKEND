from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta


class Profile(models.Model):

    def six_months_from_today():
        return datetime.now() + timedelta(days=180)
    
    UserGender = [("Male", "Male"), ("Female", "Female")]

    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile_user')
    phone = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=6, choices=UserGender, default="Male")
    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    # profile picture name
    profile_pic = models.CharField(max_length=255, null=True, blank=True)
    legal_consent_date = models.DateField(default=six_months_from_today)
