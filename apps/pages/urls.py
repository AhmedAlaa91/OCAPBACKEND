from __future__ import annotations

from django.urls import path

from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='pages.home'),

]
