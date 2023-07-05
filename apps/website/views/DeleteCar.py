from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from ..forms.CarRegistration import CarRegistrationForm
from ..models.CarRegistration import Car


def DeleteCar(request, pk=None):
    context = {}
    Carinstance = Car.objects.get(CarReg_id=pk)

    # create object of form

    form = CarRegistrationForm(instance=Carinstance)
   # if (request.method == 'POST'):
    #    form = CarRegistrationForm(request.POST , instance=Carinstance)
    # check if form data is valid
    if Carinstance:

        Carinstance.delete()

        return redirect('pages.mycars')

   # context = {'form': form, 'context': 'edit'}
   # return render(request, 'CarReg.html', context)
