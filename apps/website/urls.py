from __future__ import annotations

from django.urls import path

from .views.CarRegistration import CarRegistration
from .views.DeleteCar import DeleteCar
from .views.DisplayRegCars import DisplayRegCars
from .views.UpdateCar import UpdateCar
from apps.website.views.auth import AuthView
from apps.website.views.auth import ProfileView
from apps.website.views.ride import RideView
from apps.website.views.myRides import MyRidesListView
urlpatterns = [
    path('register/', AuthView.register, name='website.register'),
    path('login/', AuthView.login, name='website.login'),
    path('logout/', AuthView.logout, name='website.logout'),
    path('profile/', ProfileView.edit_profile, name='website.profile'),


    path('carreg/', CarRegistration, name='pages.carreg'),
    path('mycars/', DisplayRegCars, name='pages.mycars'),
    path('UpdateCar/<pk>/', UpdateCar, name='pages.UpdateCar'),
    path('DeleteCar/<pk>/', DeleteCar, name='pages.DeleteCar'),

    path('ride/', RideView.createRide, name='website.ride'),
    path('myrides/', MyRidesListView.as_view(), name='website.myrides'),

]
