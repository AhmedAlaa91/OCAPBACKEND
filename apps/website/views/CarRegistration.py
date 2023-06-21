from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from ..forms.CarRegistration import CarRegistrationForm


def CarRegistration(request):
    context = {}

    # create object of form
    form = CarRegistrationForm()

    if (request.method == 'POST'):
        form = CarRegistrationForm(request.POST)
    # check if form data is valid
        if form.is_valid():
            # save the form data to model
            form.save()

            return redirect('pages.home')

    context = {'form': form}
    return render(request, 'CarReg.html', context)
