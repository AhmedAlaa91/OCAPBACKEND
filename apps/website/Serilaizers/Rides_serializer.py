from rest_framework import serializers

from apps.website.models.profile import *
from apps.website.models.ride import *
from apps.website.models.CarRegistration import *


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



class CarPlate_serializer(serializers.ModelSerializer):

   
    class Meta:
        model = CarPlate
        fields = '__all__'


class car_serializer(serializers.ModelSerializer):

    Car_Pallet_Number=CarPlate_serializer()

    def get_Car_Pallet_Number(self, obj):
        return f'{obj.Car_Pallet_Number.number} '
    class Meta:
        model = Car
        fields = '__all__'

class RideDisplay_serializer(serializers.ModelSerializer):
    creator=User_serializer()
    car= car_serializer()
    class Meta:
        model = Ride
        fields = ['id','city','area','type','date','leave_time','return_time','Car_Pallet_Number','no_of_seats','car','creator','restrictions','meeting_point','creator']


