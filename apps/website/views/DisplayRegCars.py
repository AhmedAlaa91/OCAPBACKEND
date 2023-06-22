from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from ..models.CarRegistration import Car


def DisplayRegCars(request):
    carObj = Car.objects.filter(Owner=request.user.profile)

    if carObj:
        context = {'carObj': carObj}

    return render(request, 'Mycars.html', context)
