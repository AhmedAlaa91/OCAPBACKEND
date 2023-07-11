from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from website.models import Ride

class MyRidesListView(LoginRequiredMixin, ListView):
    template_name = "my_rides.html"

    def get_queryset(self):
        current_user = self.request.user
        return Ride.objects.filter(creator=current_user)
