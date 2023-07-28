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

        RideChecked = ride.RidesBooked.objects.filter(Requestor=request.user).values()
        found_date = ''
        found_type = ''

        if RideChecked:
            RideFound = RideChecked[0]['RideRequested_id']
            RideFoundObj = ride.Ride.objects.filter(id=RideFound).values()
            found_date = RideFoundObj[0]['date']
            found_type = RideFoundObj[0]['type']

            print(RideFoundObj[0]['date'])

        #

        rideObj = ride.Ride.objects.filter(id=rideid)

        rideFields = rideObj.values()

        source = rideFields[0]['area']
        typeRide = rideFields[0]['type']
        leaveTime = rideFields[0]['leave_time']
        leaveDate = rideFields[0]['date']
        rideCreator = rideFields[0]['creator_id']

        if (found_date != leaveDate) and (found_type != typeRide):
            ride.RidesBooked.objects.create(RideRequested=rideObj[0], Requestor=request.user)

            rideObj.update(no_of_seats=F('no_of_seats') - 1)

            passenger = User.objects.filter(username=request.user).values()
            passenger_email = passenger[0]['email']
            passenger_fullname = passenger[0]['first_name'] + ' ' + passenger[0]['last_name']
            passenger_msg = f"""Your Ride {typeRide} from {source} on {leaveDate} at {leaveTime} is Confirmed.
            
            """
            passenger_receiptants = [{"email": passenger_email, "name": passenger_fullname}]

            driver = User.objects.filter(id=rideCreator).values()
            driver_email = driver[0]['email']
            driver_fullname = driver[0]['first_name'] + ' ' + driver[0]['last_name']
            driver_msg = f""" Hello {driver_fullname} ,   {passenger_fullname} has joined Your Ride {typeRide} from {source} on {leaveDate} at {leaveTime} .
            
            """
            passenger_receiptants = [{"email": passenger_email, "name": passenger_fullname}]
            driver_receiptants = [{"email": driver_email, "name": driver_fullname}]

            # send_alerting_message (passenger_receiptants ,passenger_msg )
            # send_alerting_message (driver_receiptants ,driver_msg )

            send_alerting_message (passenger_receiptants ,passenger_msg )
            send_alerting_message (driver_receiptants ,driver_msg )




        
        return redirect('/rides')

    def CancelRide(request, rideid):
        ride.RidesBooked.objects.filter(RideRequested=rideid, Requestor=request.user).delete()
        rideObj = ride.Ride.objects.filter(id=rideid)
        rideObj.update(no_of_seats=F('no_of_seats') + 1)
        rideFields = rideObj.values()

        source = rideFields[0]['area']
        typeRide = rideFields[0]['type']
        leaveTime = rideFields[0]['leave_time']
        leaveDate = rideFields[0]['date']
        rideCreator = rideFields[0]['creator_id']

        passenger = User.objects.filter(username=request.user).values()
        passenger_email = passenger[0]['email']
        passenger_fullname = passenger[0]['first_name'] + ' ' + passenger[0]['last_name']
        passenger_msg = f"""Your Ride {typeRide} from {source} on {leaveDate} at {leaveTime} is Cancelled.
        
        """
        passenger_receiptants = [{"email": passenger_email, "name": passenger_fullname}]

        driver = User.objects.filter(id=rideCreator).values()
        driver_email = driver[0]['email']
        driver_fullname = driver[0]['first_name'] + ' ' + driver[0]['last_name']
        driver_msg = f""" Hello {driver_fullname} ,   {passenger_fullname} has Cancelled his ride {typeRide} from {source} on {leaveDate} at {leaveTime} .
        
        """
        passenger_receiptants = [{"email": passenger_email, "name": passenger_fullname}]
        driver_receiptants = [{"email": driver_email, "name": driver_fullname}]

        # send_alerting_message (passenger_receiptants ,passenger_msg )
        # send_alerting_message (driver_receiptants ,driver_msg )

        send_alerting_message (passenger_receiptants ,passenger_msg )
        send_alerting_message (driver_receiptants ,driver_msg )



        
        return redirect('/rides')
