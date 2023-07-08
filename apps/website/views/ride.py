from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from website.forms.ride import RideForm
from website.models import Car
from datetime import datetime

class RideView(View):
    context = {}
    def createRide(request):
        context = {}
        if request.method == 'GET':
            context["form"] = RideForm(request=request)
            context["context"] = "create"
            return render(request, 'ride.html', context)

        if request.method == 'POST':
            form = RideForm(request.POST) 
            if form.is_valid():
                form = form.save(commit=False)
                is_ride_two_ways = request.POST.get('is_ride_two_ways')
                if not is_ride_two_ways:
                    form.return_date = ""
                car_id = request.POST.get('car')
                car = Car.objects.filter(CarReg_id=car_id).first()
                form.car = car
                form.creator = request.user
                form.save()
                messages.success(request, 'Ride created successfully.')
                return redirect('/rides')
            else:
                return render(request, 'ride.html', {'form': form})
