from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.website.jsonData import JsonData


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"


    def get_context_data(self, **kwargs: str):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["areas"] = JsonData.get_areas()
        context["cities"] = JsonData.get_cities_json()
        context["user_area"] = self.request.user.profile.area
        context["user_city"] = self.request.user.profile.city
        return context