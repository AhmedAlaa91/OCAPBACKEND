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
            task = form.save(commit=False)
            task.Owner = request.user.profile
            task.save()

            return redirect('pages.mycars')

    context = {'form': form, 'context': 'create'}
    return render(request, 'CarReg.html', context)
