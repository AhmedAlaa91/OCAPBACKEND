from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from website.forms.ride import RideForm
from website.models import Car
import json
from pathlib import Path

class GetAreaName():
    def get_area_name(area_id):
        area_name = ""
        if area_id == "0":
            return "City Stars Office"
        current_dir = Path.cwd()
        areas_file_loc = 'static/json/areas.json'
        f = open(current_dir.joinpath(areas_file_loc), encoding='utf8')
        areas = json.load(f)['data']
        for area in areas:
            if area["id"] == area_id:
                area_name = area["city_name_en"]
                return area_name

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
                form.source = GetAreaName.get_area_name(request.POST.get('source'))
                form.destination = GetAreaName.get_area_name(request.POST.get('destination'))
                is_ride_two_ways = request.POST.get('is_ride_two_ways')
                if not is_ride_two_ways:
                    form.return_date = None
                car_id = request.POST.get('car')
                car = Car.objects.filter(CarReg_id=car_id).first()
                form.car = car
                form.creator = request.user
                form.save()
                messages.success(request, 'Ride created successfully.')
                return redirect('/myrides')
            else:
                return render(request, 'ride.html', {'form': form})
