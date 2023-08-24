from django.shortcuts import redirect

from apps.website.forms.CarRegistration import CarRegistrationForm
from apps.website.models.CarRegistration import Car


def DeleteCar(request, pk=None):
    Carinstance = Car.objects.get(CarReg_id=pk)
    if Carinstance:
        Carinstance.delete()
    return redirect("pages.mycars")
