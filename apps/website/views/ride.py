import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View
from apps.website.forms.ride import RideForm
from apps.website.models import Car

from django.contrib.auth.models import User

from apps.website.jsonData import JsonData
from apps.website.models import ride
from django.db.models import F

from lib.mail_service.mail import send_alerting_message

log = logging.getLogger(__name__)


class RideView(View):

    def createRide(request):
        context = {}

        if request.method == 'GET':
            context['form'] = RideForm(request=request)
            context['context'] = 'create'
            context['areas'] = JsonData.get_areas()
            context['cities'] = JsonData.get_cities_json()
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
                if ride_type == 'To Office' or ride_type == 'From Office':
                    form.return_time = None
                car_id = request.POST.get('car')
                car = Car.objects.filter(CarReg_id=car_id).first()
                form.car = car
                form.creator = request.user
                form.save()
                ride.RidesBooked.objects.create(RideRequested=form, Requestor=request.user)
                messages.success(request, 'Ride created successfully.')
                log.info(f'Ride created successfully NO:{form.pk}')
                return redirect('/myrides')
            else:
                return render(request, 'ride.html', {'form': form})

    def RequestRide(request, rideid):

        booked_rides = ride.RidesBooked.objects.filter(Requestor=request.user)
        rideObj = ride.Ride.objects.filter(id=rideid).first()

        for bookded_ride in booked_rides:
            if bookded_ride.RideRequested.type == rideObj.type and bookded_ride.RideRequested.date == rideObj.date:
                return redirect('/rides')

        ride.RidesBooked.objects.create(RideRequested=rideObj, Requestor=request.user)

        rideObj.no_of_seats -= 1
        rideObj.save()

        passenger = User.objects.filter(username=request.user).values()[0]
        driver = User.objects.filter(id=rideObj.creator.id).values()[0]

        passenger_details = {
            "user": passenger['first_name'] + ' ' + passenger['last_name'],
            "content_header": "Your ride request is Confirmed.",
            "ride_type": rideObj.type,
            "ride_time": f"""{rideObj.date} {rideObj.leave_time}""",
            "ride_meeting_point": rideObj.meeting_point,
            "ride_restrictions": rideObj.restrictions,
            "ride_owner": driver['first_name'] + ' ' + driver['last_name'],
            "ride_car_model": rideObj.car.Car_Manufacture,
            "ride_car_color": rideObj.car.Car_Color,
            "ride_car_plate_number": rideObj.car.Car_Pallet_Number,
        }

        driver_details = {
            "user": driver['first_name'] + ' ' + driver['last_name'],
            "content_header": passenger['first_name'] + ' ' + passenger['last_name'] + " has joined your ride.",
            "ride_type": rideObj.type,
            "ride_time": f"""{rideObj.date} {rideObj.leave_time}""",
        }

        send_alerting_message ([{"email": passenger['email'], "name": passenger['first_name'] + ' ' + passenger['last_name']}] , content=passenger_details, subject="Ride Confirmation")
        send_alerting_message ([{"email": driver['email'], "name": driver['first_name'] + ' ' + driver['last_name']}] , content=driver_details, subject="Ride Confirmation")
        
        return redirect(request.META.get('HTTP_REFERER'), request.GET)

    def CancelRide(request, rideid):
        """
        This should cancel request for a specific ride (CancelRequest)
        """
        ride.RidesBooked.objects.filter(RideRequested=rideid, Requestor=request.user).delete()
        rideObj = ride.Ride.objects.filter(id=rideid)
        rideObj.update(no_of_seats=F('no_of_seats') + 1)
        rideFields = rideObj.values()

        source = rideFields[0]['area']
        typeRide = rideFields[0]['type']
        leaveTime = rideFields[0]['leave_time']
        leaveDate = rideFields[0]['date']
        rideCreator = rideFields[0]['creator_id']

        passenger = User.objects.filter(username=request.user).values()[0]
        driver = User.objects.filter(id=rideCreator).values()[0]

        passenger_details = {
            "user": passenger['first_name'] + ' ' + passenger['last_name'],
            "content_header": "Your ride request is Cancelled.",
            "ride_type": typeRide,
            "ride_time": f"""{leaveDate} {leaveTime}""",
            "ride_meeting_point": rideObj[0].meeting_point,
            "ride_restrictions": rideObj[0].restrictions,
            "ride_owner": driver['first_name'] + ' ' + driver['last_name'],
            "ride_car_model": rideObj[0].car.Car_Manufacture,
            "ride_car_color": rideObj[0].car.Car_Color,
            "ride_car_plate_number": rideObj[0].car.Car_Pallet_Number,
        }

        driver_details = {
            "user": driver['first_name'] + ' ' + driver['last_name'],
            "content_header": passenger['first_name'] + ' ' + passenger['last_name'] + " has cancelled ride request.",
            "ride_type": typeRide,
            "ride_time": f"""{leaveDate} {leaveTime}""",
        }

        send_alerting_message ([{"email": passenger['email'], "name": passenger['first_name'] + ' ' + passenger['last_name']}] , content=passenger_details, subject="Ride Cancellation")
        send_alerting_message ([{"email": driver['email'], "name": driver['first_name'] + ' ' + driver['last_name']}] , content=driver_details, subject="Ride Cancellation")



        
        return redirect(request.META.get('HTTP_REFERER'))

