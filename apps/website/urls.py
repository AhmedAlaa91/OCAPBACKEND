from django.urls import path, re_path
from apps.website.views.CarRegistration import CarRegistration
from apps.website.views.DeleteCar import DeleteCar
from apps.website.views.DisplayRegCars import DisplayRegCars
from apps.website.views.UpdateCar import UpdateCar
from apps.website.views.auth import AuthView
from apps.website.views.auth import ProfileView
from apps.website.views.ride import RideView
from apps.website.views.myRides import MyRidesListView
from apps.website.views.DisplayRides import get_context_data
from apps.website.views.edit_ride import EditRideView

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
    path('reqrides/<rideid>/', RideView.RequestRide, name='pages.reqride'),
    path('cancelrides/<rideid>/', RideView.CancelRide, name='pages.cancelride'),
    path('rides/', get_context_data, name='pages.rides'),
    re_path('rides/(?P<city>)/(?P<area>)$', get_context_data, name='pages.rides'),
    path('rides/update/<pk>', EditRideView.as_view(), name='pages.update_ride'),

]
