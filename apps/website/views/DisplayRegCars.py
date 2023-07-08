from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from ..models.CarRegistration import Car


def DisplayRegCars(request):
    carObj = Car.objects.filter(Owner=request.user)

    if carObj:
        context = {'carObj': carObj}
    else:
        context = {'carObj': 'carObj'}

    return render(request, 'MyCars.html', context)
