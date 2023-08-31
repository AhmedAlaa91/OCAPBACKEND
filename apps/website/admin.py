from django.contrib import admin

from apps.website.models.CarRegistration import Car, CarPlate
from apps.website.models.profile import Profile
from apps.website.models.ride import Ride, RidesBooked

# Register your models here.
admin.site.register(Ride)
admin.site.register(RidesBooked)
admin.site.register(Car)
admin.site.register(CarPlate)
admin.site.register(Profile)
