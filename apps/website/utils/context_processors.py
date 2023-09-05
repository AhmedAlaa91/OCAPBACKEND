# coding: utf-8
from apps.website.models import Ride


def portal_total_emissions(request):
    ctx = {'total_emissions': Ride.objects.get_total_carbon_emissions()}
    return ctx
