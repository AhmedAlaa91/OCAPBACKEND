import datetime
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from apps.website.models import Ride, RidesBooked


class MyRidesListView(LoginRequiredMixin, ListView):
    template_name = "my_rides.html"

    current_date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    def get_context_data(self, **kwargs: str):
        current_user = self.request.user
        context = super(MyRidesListView, self).get_context_data(**kwargs)
        past_rides = Q(date__lt=self.current_date) | Q(
            Q(date=self.current_date) & Q(leave_time__lte=self.current_time)
        )
        past_booked_rides = Q(RideRequested__date__lt=self.current_date) | Q(
            Q(RideRequested__date=self.current_date) & Q(RideRequested__leave_time__lte=self.current_time)
        )

        created_historical_rides = Ride.objects.filter(Q(creator=current_user) & (past_rides)).all()

        joined_historical_rides = Ride.objects.none()
        joined_historical_rides_booked = (
            RidesBooked.objects.select_related().filter(Q(Requestor=current_user) & (past_booked_rides)).all()
        )
        for item in joined_historical_rides_booked:
            joined_historical_rides |= Ride.objects.filter(pk=item.RideRequested.id)

        result = joined_historical_rides | created_historical_rides

        context["historical_rides"] = result
        return context

    def get_queryset(self):
        current_user = self.request.user
        comming_rides = Q(date__gt=self.current_date) | Q(
            Q(date=self.current_date) & Q(leave_time__gte=self.current_time)
        )
        comming_booked_rides = Q(RideRequested__date__gt=self.current_date) | Q(
            Q(RideRequested__date=self.current_date) & Q(RideRequested__leave_time__gte=self.current_time)
        )

        created_planned_rides = Ride.objects.filter(Q(creator=current_user) & (comming_rides)).all()

        joined_planned_rides = Ride.objects.none()
        joined_planned_rides_booked = (
            RidesBooked.objects.select_related()
            .filter(Q(Requestor=current_user) & (comming_booked_rides))
            .all()
        )
        for item in joined_planned_rides_booked:
            joined_planned_rides |= Ride.objects.filter(pk=item.RideRequested.id)

        result = joined_planned_rides | created_planned_rides
        return result
