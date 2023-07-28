from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.website.models import RidesBooked
from django.db.models import Q
import datetime


class MyRidesListView(LoginRequiredMixin, ListView):
    template_name = "my_rides.html"

    current_date = datetime.date.today()
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    def get_context_data(self, **kwargs: str):
        current_user = self.request.user
        context = super(MyRidesListView, self).get_context_data(**kwargs)
        historical_rides = RidesBooked.objects.select_related().filter(Q(Requestor=current_user) & (
                Q(RideRequested__date__lt=self.current_date) |
                Q(Q(RideRequested__date=self.current_date) &
                  Q(RideRequested__leave_time__lte=self.current_time))))

        context["historical_rides"] = historical_rides
        return context

    def get_queryset(self):
        current_user = self.request.user
        planned_rides = RidesBooked.objects.select_related().filter(Q(Requestor=current_user) & (
                Q(RideRequested__date__gt=self.current_date) |
                Q(Q(RideRequested__date=self.current_date) &
                  Q(RideRequested__leave_time__gte=self.current_time))))
        return planned_rides
