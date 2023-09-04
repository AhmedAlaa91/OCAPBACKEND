from rest_framework import serializers

from apps.website.models.rides_booked import *

from .Rides_serializer import Ride_serializer, User_serializer


class BookedRides_serializer(serializers.ModelSerializer):
    RideRequested_id = Ride_serializer(source="RideRequested", read_only=True)
    Requestor_id = User_serializer(source="Requestor", read_only=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = RidesBooked
        fields = ["RideRequested_id", "Requestor_id", "status", "comment"]

    def get_status(self, obj):
        return obj.get_status_display()


class BookedRidesUpdate_serializer(serializers.ModelSerializer):
    class Meta:
        model = RidesBooked
        fields = ["RideRequested_id", "Requestor_id", "status", "comment"]
