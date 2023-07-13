from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from django.db.models import Prefetch

from ..models.ride import Ride
from ..models.CarRegistration import Car , CarPlate

def DisplayRides(request):


    RideObj =Ride.objects.filter(creator=request.user).select_related("car")
    
    if RideObj:
        context = {'RideObj': RideObj}
    else:
        context = {'RideObj': 'RideObj'}


    return render(request, 'DisplayRides.html', context)
