from rest_framework import serializers

from apps.website.models.profile import *
from apps.website.models.ride import *


class Ride_serializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["id"]


class Profile_serializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "gender", "phone", "profile_pic"]

    def get_profile_pic(self, obj):
        return obj.get_profile_picture_url()


class User_serializer(serializers.ModelSerializer):
    profile = Profile_serializer()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "profile"]
