from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from website.forms.ride import RideForm
from website.models import Car
import json
from pathlib import Path

class RideView(View):
    def get_area_name(area_id):
        area_name = ""
        current_dir = Path.cwd()
        areas_file_loc = 'static/json/areas.json'
        f = open(current_dir.joinpath(areas_file_loc), encoding='utf8')
        areas = json.load(f)['data']
        for area in areas:
            if area["id"] == area_id:
                area_name = area["city_name_en"]
                return area_name

    def get_city_name(city_id):
        city_name = ""
        current_dir = Path.cwd()
        cities_file_loc = 'static/json/cities.json'
        f = open(current_dir.joinpath(cities_file_loc), encoding='utf8')
        cities = json.load(f)['data']
        for city in cities:
            if city["id"] == city_id:
                city_name = city["governorate_name_en"]
                return city_name

    def get_areas():
        current_dir = Path.cwd()
        areas_file_loc = 'static/json/areas.json'
        f = open(current_dir.joinpath(areas_file_loc), encoding='utf8')
        areas = json.load(f)['data']
        f.close()
        return areas
 
    def createRide(request):
        context = {}
        
        if request.method == 'GET':
            context["form"] = RideForm(request=request)
            context["context"] = "create"
            context['areas'] = RideView.get_areas()
            context['user_area'] = request.user.profile.area
            context['user_city'] = request.user.profile.city
            return render(request, 'ride.html', context)

        if request.method == 'POST':
            form = RideForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.city = RideView.get_city_name(request.POST.get('city'))
                form.area = RideView.get_area_name(request.POST.get('area'))
                ride_type = request.POST.get('ride_type')
                form.type = ride_type
                if ride_type == "To Office" or ride_type == "From Office" :
                    form.return_time = None
                car_id = request.POST.get('car')
                car = Car.objects.filter(CarReg_id=car_id).first()
                form.car = car
                form.creator = request.user
                form.save()
                messages.success(request, 'Ride created successfully.')
                return redirect('/myrides')
            else:
                return render(request, 'ride.html', {'form': form})
