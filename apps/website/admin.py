from django.contrib import admin
from apps.website.models.ride import Ride
from apps.website.models.ride import RidesBooked
from apps.website.models.CarRegistration import Car
from apps.website.models.CarRegistration import CarPlate
from apps.website.models.profile import Profile

# Register your models here.
admin.site.register(Ride)
admin.site.register(RidesBooked)
admin.site.register(Car)
admin.site.register(CarPlate)
admin.site.register(Profile)
