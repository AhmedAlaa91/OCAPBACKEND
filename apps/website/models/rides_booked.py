import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from lib.utils import Average

from .CarRegistration import Car
from .ride import Ride

log = logging.getLogger(__name__)


class RidesBooked(models.Model):
    request_status = [("1", "Pending"), ("2", "Accepted"), ("3", "Rejected"), ("4", "Cancelled")]
    Requestor = models.ForeignKey(User, on_delete=models.CASCADE)
    RideRequested = models.ForeignKey(Ride, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=request_status, default="1")
    comment = models.CharField(max_length=50, null=True, blank=True)

    @property
    def calculate_car_emission(self):
        try:
            ride_passengers = RidesBooked.objects.get_passengers_from_ride(ride_id=self.RideRequested.pk)
            log.info(f"No of requesters returned {len(ride_passengers)}")
            total_fuel_consumption = list()
            for ride_passenger in ride_passengers:
                cars = Car.objects.get_user_cars(user=ride_passenger.Requestor)

                if len(cars) == 0:
                    total_fuel_consumption.append(settings.AVERAGE_CARS_CONSUMPTION_PER_100KM)
                elif len(cars) == 1:
                    car_obj = cars.first()
                    total_fuel_consumption.append(car_obj.fuel_cons)
                else:
                    average_user_cars = list()
                    for car in cars:
                        average_user_cars.append(car.Fuel_consumption)
                    avg = Average(average_user_cars)
                    total_fuel_consumption.append(avg)
            all_saved_fuel_consumption = sum(total_fuel_consumption)
            # distance will be calculated in ride model
            per_km_consumption = all_saved_fuel_consumption / 100
            distance_average_saved_fuel = per_km_consumption * self.RideRequested.distance
            result = distance_average_saved_fuel * settings.AVERAGE_EMISSIONS_PER_LITRE
            log.info(f"Ride No{self.RideRequested.pk} have saved emissions {result}")
            return result
        except Exception as ex:
            log.error(f"{str(ex)}")
            return None
