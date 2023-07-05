from __future__ import annotations

from django.urls import path

from .views.CarRegistration import CarRegistration
from .views.DeleteCar import DeleteCar
from .views.DisplayRegCars import DisplayRegCars
from .views.UpdateCar import UpdateCar
from apps.website.views.auth import AuthView
from apps.website.views.auth import ProfileView
urlpatterns = [
    path('register/', AuthView.register, name='website.register'),
    path('login/', AuthView.login, name='website.login'),
    path('logout/', AuthView.logout, name='website.logout'),
    path('profile/', ProfileView.edit_profile, name='website.profile'),


    path('carreg/', CarRegistration, name='pages.carreg'),
    path('mycars/', DisplayRegCars, name='pages.mycars'),
    path('UpdateCar/<pk>/', UpdateCar, name='pages.UpdateCar'),
    path('DeleteCar/<pk>/', DeleteCar, name='pages.DeleteCar'),

]
