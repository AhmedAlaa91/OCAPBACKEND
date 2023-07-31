from django.views.generic import UpdateView
from apps.website.models.ride import Ride
from apps.website.models.ride import RidesBooked
from apps.website.models import Car
from apps.website.forms.ride import RideForm
from apps.website.jsonData import JsonData
import logging
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import F
from lib.mail_service.mail import send_alerting_message

log = logging.getLogger(__name__)


class EditRideView(UpdateView):
    """
    A View To Edit Ride Information and also alert passengers with mail notification
    """
    model = Ride
    form_class = RideForm
    template_name = 'ride.html'
    current_object = None

    def get_object(self, queryset=None):
        queryset = Ride.objects.filter(pk=self.kwargs['pk']).first()
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super(EditRideView, self).get_context_data(**kwargs)
        # Add data needed to Update Rider
        ctx['form'] = RideForm(request=self.request, instance=self.object)
        ctx['context'] = 'edit'
        ctx['areas'] = JsonData.get_areas()
        ctx['cities'] = JsonData.get_cities_json()
        ctx['user_area'] = self.request.user.profile.area
        ctx['user_city'] = self.request.user.profile.city
        return ctx

    def form_valid(self, form, **kwargs):
        print('hello')
        try:
            ride = self.object
            ride_booked = RidesBooked.objects.filter(RideRequested=ride, Requestor=self.request.user).first()
            ride.city = JsonData.get_city_name(self.request.POST.get('city')) if self.request.POST.get(
                'city') else self.object.city
            ride.area = JsonData.get_area_name(self.request.POST.get('area')) if self.request.POST.get(
                'area') else self.object.area
            ride_type = self.request.POST.get('ride_type')
            ride.type = ride_type
            if ride_type == 'To Office' or ride_type == 'From Office':
                ride.return_time = None
            car_id = self.request.POST.get('car')
            car = Car.objects.filter(CarReg_id=car_id).first()
            ride.car = car
            ride.creator = self.request.user
            ride.save()
            ride_booked.RideRequested = ride
            ride_booked.Requestor = self.request.user
            ride_booked.save()
            messages.success(self.request, 'Ride updated successfully.')
            log.info(f'Ride updated successfully NO:{ride.pk}')
        except Exception as ex:
            log.info(f'Error : {str(ex)}')
            messages.error(self.request, f'Error{str(ex)}')
        finally:
            return super().form_valid(form)

    def get_success_url(self, **kwargs):
        try:
            rideObj = Ride.objects.filter(pk=self.kwargs['pk']).first()
            source = rideObj.area
            typeRide = rideObj.type
            leaveTime = rideObj.leave_time
            leaveDate = rideObj.date
            rides = RidesBooked.objects.filter(RideRequested=rideObj).exclude(Requestor=self.request.user)
            for ride in rides:
                passenger_email = ride.Requestor.email
                passenger_fullname = ride.Requestor.first_name + ' ' + ride.Requestor.last_name
                passenger_msg = f"""Your Ride {typeRide} from {source} on {leaveDate} at {leaveTime} have been Updated.

                            """
                passenger_receiptants = [{"email": passenger_email, "name": passenger_fullname}]
                send_alerting_message(passenger_receiptants, passenger_msg)
                log.info(f'Alert had been sent to:{ride.Requestor.email}')
            messages.success(self.request, 'Alert Messages had been sent to passengers.')
        except Exception as ex:
            log.info(f'Error in sending mails : {str(ex)}')
            messages.error(self.request, f'Error in sending alerts{str(ex)}')
        finally:
            return reverse('website.myrides')
