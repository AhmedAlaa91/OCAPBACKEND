from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from website.forms.ride import RideForm
from website.models import Car
from apps.website.jsonData import JsonData

class RideView(View):
 
    def createRide(request):
        context = {}
        
        if request.method == 'GET':
            context["form"] = RideForm(request=request)
            context["context"] = "create"
            context['areas'] = JsonData.get_areas()
            context['user_area'] = request.user.profile.area
            context['user_city'] = request.user.profile.city
            return render(request, 'ride.html', context)

        if request.method == 'POST':
            form = RideForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.city = JsonData.get_city_name(request.POST.get('city'))
                form.area = JsonData.get_area_name(request.POST.get('area'))
                ride_type = request.POST.get('ride_type')
                form.type = ride_type
                if ride_type == "To Office" or ride_type == "From Office":
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
