from __future__ import annotations

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home.html'
