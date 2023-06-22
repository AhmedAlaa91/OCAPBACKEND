from __future__ import annotations

from django.urls import path

from .views.CarRegistration import CarRegistration
from apps.website.views import AuthView
from apps.website.views import ProfileView
urlpatterns = [
    path('register/', AuthView.register, name='website.register'),
    path('login/', AuthView.login, name='website.login'),
    path('logout/', AuthView.logout, name='website.logout'),
    path('profile/', ProfileView.edit_profile, name='website.profile'),


    path('carreg/', CarRegistration, name='pages.carreg'),

]
