from django.db import models


class RideBookedManager(models.Manager):

    def get_accepted_passengers_from_ride(self, *args, **kwargs):
        """
             get accepted passengers for a specific ride
        """
        ride_id = None
        for key, value in kwargs.items():
            if key == "ride_id":
                ride_id = value
        return super().get_queryset().filter(RideRequested__pk=ride_id, status="2")
