from django.views.generic import UpdateView
from apps.website.models.ride import Ride
from apps.website.models.ride import RidesBooked
from apps.website.models import Car
from apps.website.forms.ride import RideForm
from apps.website.jsonData import JsonData
import logging
from django.contrib import messages
from django.shortcuts import redirect

log = logging.getLogger(__name__)


class EditRideView(UpdateView):
    """
    A View To Edit Ride Information and also alert passengers with mail notification
    """
    model = Ride
    form_class = RideForm
    template_name = 'ride.html'

    def get_context_data(self, **kwargs):
        ctx = super(EditRideView, self).get_context_data(**kwargs)
        # Add data needed to Update Rider
        ctx['context'] = 'create'
        ctx['areas'] = JsonData.get_areas()
        ctx['user_area'] = self.request.user.profile.area
        ctx['user_city'] = self.request.user.profile.city
        return ctx

    def form_valid(self, form):
        try:
            form = form.save(commit=False)
            form.city = JsonData.get_city_name(self.request.POST.get('city'))
            form.area = JsonData.get_area_name(self.request.POST.get('area'))
            ride_type = self.request.POST.get('ride_type')
            form.type = ride_type
            if ride_type == 'To Office' or ride_type == 'From Office':
                form.return_time = None
            car_id = self.request.POST.get('car')
            car = Car.objects.filter(CarReg_id=car_id).first()
            form.car = car
            form.creator = self.request.user
            form.save()
            RidesBooked.objects.create(RideRequested=form, Requestor=self.request.user)
            messages.success(self.request, 'Ride created successfully.')
            log.info(f'Ride created successfully NO:{form.pk}')
        except Exception as ex:
            log.info(f'Ride created successfully NO:{form.pk}')
            messages.error(self.request, f'Error{str(ex)}')
        finally:
            return super().form_valid(form)

    def get_success_url(self):
        return redirect('pages.rides')
