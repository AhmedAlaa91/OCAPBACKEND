import logging

from django.shortcuts import redirect, render

from ..forms.CarRegistration import CarRegistrationForm , CarPlateForm
from ..models.CarRegistration import Car , CarPlate

log = logging.getLogger(__name__)


def UpdateCar(request, pk=None):
    context = {}
    Carinstance = Car.objects.get(CarReg_id=pk)
    Plateinstance = CarPlate.objects.get(CarPlate_id=Carinstance.Car_Pallet_Number_id)
    
    # create object of form

    form = CarRegistrationForm(instance=Carinstance)
    Plate_form = CarPlateForm(instance=Plateinstance)
    if request.method == "POST":
        form = CarRegistrationForm(request.POST, instance=Carinstance)
        Plate_form = CarPlateForm(request.POST,instance=Plateinstance)
        # check if form data is valid
        if form.is_valid() and Plate_form.is_valid():
            # save the form data to model
            task = form.save(commit=False)
            task.save()
            plate_task = Plate_form.save(commit=False)
            plate_task.save()
            log.info(f"a car had been created and inserted into db CAR:{task.Car_Pallet_Number}")
            return redirect("pages.mycars")

    context = {"form": form,"form2":Plate_form ,"context": "edit"}
    return render(request, "CarReg.html", context)
