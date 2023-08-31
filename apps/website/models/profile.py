from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static

from lib.s3_storage.s3_helpers import get_profile_pic_by_key


class Profile(models.Model):
    def six_months_from_today():
        return datetime.now() + timedelta(days=180)

    UserGender = [("Male", "Male"), ("Female", "Female")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=6, choices=UserGender, default="Male")
    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    # profile picture name
    profile_pic = models.CharField(max_length=255, null=True, blank=True)
    legal_consent_date = models.DateField(default=six_months_from_today)

    def get_profile_picture_url(self):
        if self.profile_pic == None:
            if self.gender == "Male":
                return static("images/male.jfif")
            else:
                return static("images/female.jfif")
        else:
            return get_profile_pic_by_key(key=self.profile_pic)
