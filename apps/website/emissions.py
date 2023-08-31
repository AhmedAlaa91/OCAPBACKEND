import logging

from django.conf import settings

from apps.website.models import Car, Ride, RidesBooked

log = logging.getLogger(__name__)


def Average(lst):
    return sum(lst) / len(lst)


def calculate_car_emission(ride: Ride):
    try:
        ride_passengers = RidesBooked.objects.get_passengers_from_ride(ride_id=ride.pk)
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
                    average_user_cars.append(car.fuel_cons)
                avg = Average(average_user_cars)
                total_fuel_consumption.append(avg)
        all_saved_fuel_consumption = sum(total_fuel_consumption)
        # distance will be calculated in ride model
        per_km_consumption = all_saved_fuel_consumption / 100
        distance_average_saved_fuel = per_km_consumption * ride.distance
        result = distance_average_saved_fuel * settings.AVERAGE_EMISSIONS_PER_LITRE
        log.info(f"Ride No{ride.pk} have saved emissions {result}")
        # save saved emissions result in Ride emission model
        ride_emissions_obj = None
        return ride_emissions_obj
    except Exception as ex:
        log.error(f"{str(ex)}")
        return None
