from __future__ import annotations

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from django.db.models import Prefetch

from ..models.ride import Ride , RidesBooked
from ..models.CarRegistration import Car , CarPlate
from apps.website.jsonData import JsonData

def get_context_data(request, *args, **kwargs):
    area_r = request.GET.get('area')
    city_r= request.GET.get('city')
    


    if area_r and city_r :
        RideObj =Ride.objects.filter(area=area_r , city=city_r).select_related("car")


    
    elif area_r :
        RideObj =Ride.objects.filter(area=area_r ).select_related("car")
        

    elif city_r :
        RideObj =Ride.objects.filter(city=city_r).select_related("car")
       
    else :
        RideObj =Ride.objects.all()
    
    if RideObj:
        context = {'RideObj': RideObj}
    else:
        context = {'RideObj': None }
    
    
    context['areas'] = JsonData.get_areas()

    context['cities'] = JsonData.get_cities()

    context['user_area'] = request.user.profile.area
    context['user_city'] = request.user.profile.city
    
    if area_r :   context['user_area']=area_r
    if city_r :   context['user_city']=city_r


    BookedRides=[]

    for r in RideObj :

       
        BookedRideObj =RidesBooked.objects.filter(RideRequested=r.id , Requestor=request.user)
      
        if BookedRideObj :  BookedRides.append(BookedRideObj.values())
    

    context['BookedRides']=BookedRides

    print(context['BookedRides'])

  
    return render(request, 'DisplayRides.html', context)

