from datetime import date

from django.shortcuts import render

from apps.website.jsonData import JsonData
from apps.website.models.ride import Ride 
from apps.website.models.profile import Profile 
from apps.website.models.rides_booked import RidesBooked


from apps.website.Serilaizers.RidesBooked_Serializer import BookedRides_serializer

from apps.website.Serilaizers.Rides_serializer import  Profile_serializer ,RideDisplay_serializer
def get_context_data(request, *args, **kwargs):
    area_r = request.GET.get("area")
    city_r = request.GET.get("city")

    today = date.today()

    if area_r and city_r:
        if area_r == "All":
            RideObj = Ride.objects.filter(city=city_r).select_related("car")
        elif city_r == "All":
            RideObj = Ride.objects.all().select_related("car")

        else:
            RideObj = Ride.objects.filter(area=area_r, city=city_r).select_related("car")

    elif area_r:
        if area_r == "All":
            RideObj = Ride.objects.filter(city=city_r).select_related("car")

        else:
            RideObj = Ride.objects.filter(area=area_r).select_related("car")

    elif city_r:
        if city_r == "All":
            RideObj = Ride.objects.all().select_related("car")

        else:
            RideObj = Ride.objects.filter(city=city_r).select_related("car")

    else:
        RideObj = Ride.objects.all()

    RideObj = RideObj.filter(date__gte=today).exclude(ridesbooked__status__in=[3,4]).exclude(creator=request.user)
    
    RideObj_data_serialized = RideDisplay_serializer(RideObj, many=True).data

    if RideObj_data_serialized:
        context = {"RideObj": RideObj_data_serialized}
    else:
        context = {"RideObj": None}


    context["areas"] = sorted(JsonData.get_areas(), key=lambda x: x["city_name_en"])
    context["cities"] = JsonData.get_cities()

    context["user_area"] = "Choose Area"
    context["user_city"] = "Choose City"

    if area_r:
        context["user_area"] = area_r
    if city_r:
        context["user_city"] = city_r

    BookedRides = []

    for r in RideObj.values():
        BookedRideObj = RidesBooked.objects.filter(RideRequested_id=r["id"], Requestor=request.user).exclude(status__in=[3,4])

     
        if BookedRideObj:
             BookedRides.append(BookedRideObj.values())
      
    context["BookedRides"] = BookedRides

   

    return render(request, "DisplayRides.html", context)
