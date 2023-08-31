from rest_framework import serializers
from apps.website.models.ride import *

from apps.website.models.profile import *


class Ride_serializer(serializers.ModelSerializer):
  
    class Meta:
        model = Ride
        fields=['id']


class Profile_serializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields=['id','gender','phone']


class User_serializer(serializers.ModelSerializer):
    profile = Profile_serializer()
    class Meta:
        model = User
        fields=['id','first_name','last_name','profile']

