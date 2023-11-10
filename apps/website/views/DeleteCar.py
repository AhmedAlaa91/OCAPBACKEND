from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from apps.website.forms.CarRegistration import CarRegistrationForm
from apps.website.models.carregistration import Car


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

        return redirect("pages.mycars")


# context = {'form': form, 'context': 'edit'}
# return render(request, 'CarReg.html', context)
