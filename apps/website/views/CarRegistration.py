from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from ..forms.CarRegistration import CarPlateForm
from ..forms.CarRegistration import CarRegistrationForm


def CarRegistration(request):
    context = {}

    # create object of form
    form = CarRegistrationForm()
    form2 = CarPlateForm()
    if (request.method == 'POST'):
        form2 = CarPlateForm(request.POST)
        form = CarRegistrationForm(request.POST)
        # save the form data to model

    # check if form data is valid
        if form.is_valid() and form2.is_valid():
            # save the form data to model
            form2 = form2.save(commit=False)
            form2.save()

            task = form.save(commit=False)
            task.Owner = request.user.profile
            task.Car_Pallet_Number = form2
            task.save()

            return redirect('pages.mycars')

    context = {'form': form, 'form2': form2, 'context': 'create'}
    return render(request, 'CarReg.html', context)