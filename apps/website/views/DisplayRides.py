from django.shortcuts import render
from apps.website.models.ride import Ride, RidesBooked
from apps.website.jsonData import JsonData

from datetime import date


def get_context_data(request, *args, **kwargs):
    area_r = request.GET.get('area')
    city_r = request.GET.get('city')

    today = date.today()

    if area_r and city_r:
        if area_r == 'All':
            RideObj = Ride.objects.filter(city=city_r).select_related("car")
        elif city_r == 'All':
            RideObj = Ride.objects.all().select_related("car")

        else:
            RideObj = Ride.objects.filter(area=area_r, city=city_r).select_related("car")

    elif area_r:
        if area_r == 'All':
            RideObj = Ride.objects.filter(city=city_r).select_related("car")

        else:
            RideObj = Ride.objects.filter(area=area_r).select_related("car")

    # elif city_r :
    #   if city_r=='All':
    #        RideObj =Ride.objects.all().select_related("car")

    #    else :
    #           RideObj =Ride.objects.filter(city=city_r).select_related("car")

    else:
        RideObj = Ride.objects.all()

    RideObj = RideObj.filter(date__gte=today).exclude(creator=request.user)

    RideObj=RideObj.filter(date__gte= today )
    
    if RideObj:
        context = {'RideObj': RideObj}
    else:
        context = {'RideObj': None}

    context['areas'] = sorted(JsonData.get_areas(), key=lambda x: x['city_name_en'])
    context['cities'] = JsonData.get_cities()

    context['user_area'] = 'Choose Area'
    context['user_city'] = 'Choose City'

    if area_r:   context['user_area'] = area_r
    if city_r:   context['user_city'] = city_r

    BookedRides = []

    for r in RideObj.values():

        BookedRideObj = RidesBooked.objects.filter(RideRequested_id=r['id'], Requestor=request.user)

        if BookedRideObj:  BookedRides.append(BookedRideObj.values())

    context['BookedRides'] = BookedRides

    return render(request, 'DisplayRides.html', context)
