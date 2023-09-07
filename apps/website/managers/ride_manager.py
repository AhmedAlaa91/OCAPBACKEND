from django.db import models


class RideManager(models.Manager):
    def get_rides_per_current_month(self, *args, **kwargs):
        """
        return rides based on current month
        """
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year
        return super().get_queryset().filter(creator__year__gte=current_year, creator__month__gte=current_month)

    def get_rides_for_certain_user(self, *args, **kwargs):
        """
        filter rides based on user
        """
        user = None
        for key, value in kwargs.items():
            if key == "user":
                ride_id = value
        return super().get_queryset().filter(creator=user)

    def get_total_carbon_emissions(self, *args, **kwargs):
        """
              return total carbon emissions for all rides
        """
        from apps.website.utils.car_emissions import calculate_car_emission
        total_co2_emissions = int()
        all_rides = super().get_queryset().all()
        for ride in all_rides:
            co_emissions_for_ride = calculate_car_emission(ride.pk)
            if co_emissions_for_ride is not None:
                total_co2_emissions += co_emissions_for_ride
        return total_co2_emissions

