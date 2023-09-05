import logging

from django.conf import settings

from apps.website.jsonData import JsonData
from apps.website.models import Ride, RidesBooked

log = logging.getLogger(__name__)


def calculate_car_emission(ride_id):
    try:
        ride_passengers = RidesBooked.objects.get_accepted_passengers_from_ride(ride_id=ride_id)
        ride_obj = Ride.objects.get(pk=ride_id)
        if ride_obj.distance is not None:
            log.info(f"No of requesters returned {len(ride_passengers)}")
            distance = ride_obj.distance
        else:
            distance = JsonData.get_distance_by_area(ride_obj.area)
        fuel_saved = distance * settings.AVERAGE_CARS_CONSUMPTION_PER_KM * len(ride_passengers)
        carbon_saved = fuel_saved * settings.AVERAGE_EMISSIONS_PER_LITRE
        return carbon_saved

    except Exception as ex:
        log.error(f"{str(ex)}")
        return None
