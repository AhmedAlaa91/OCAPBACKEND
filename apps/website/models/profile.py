from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static

from lib.s3_storage.s3_helpers import get_profile_pic_by_key


class Profile(models.Model):
    UserGender = [("Male", "Male"), ("Female", "Female")]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=6, choices=UserGender, default="Male")
    city = models.CharField(max_length=50, null=True, blank=True)
    area = models.CharField(max_length=50, null=True, blank=True)
    # profile picture name
    profile_pic = models.CharField(max_length=255, null=True, blank=True)

    def get_profile_picture_url(self):
        if len(self.profile_pic) == 0:
            if self.gender == "Male":
                return static("images/male.png")
            else:
                return static("images/woman.png")
        else:
            return get_profile_pic_by_key(key=self.profile_pic)
