from __future__ import annotations

import json
from pathlib import Path
from .widgets import DatePickerInput, TimePickerInput
from website.models import Ride
from django import forms
from django.forms import CharField, Select, TextInput, ModelChoiceField, NumberInput
from website.models import Car
from datetime import datetime, timedelta, time

class RideForm(forms.ModelForm):

    def get_initial_date():
        return datetime.today() + timedelta(days=1)

    def get_user_areas(self, user_city):

        current_dir = Path.cwd()

        areas_file_loc = 'static/json/areas.json'

        f = open(current_dir.joinpath(areas_file_loc), encoding='utf8')

        areas_json = json.load(f)

        f.close()

        areas = []

        for area in areas_json['data']:

            if  area['governorate_id'] == user_city:

                area_tuple = tuple([area['id'], area['city_name_en']])

                areas.append(area_tuple)

        return areas
    
 
    def get_cities():

        current_dir = Path.cwd()

        cities_file_loc = 'static/json/cities.json'

        f = open(current_dir.joinpath(cities_file_loc), encoding='utf8')

        cities_json = json.load(f)

        f.close()

        cities = []

        for city in cities_json['data']:

            city_tuple = tuple([city['id'], city['governorate_name_en']])

            cities.append(city_tuple)

        return cities

    date =  CharField(initial=get_initial_date(),widget=DatePickerInput(format='%Y-%m-%d'))
    leave_time =  CharField(initial= time(8), widget=TimePickerInput(format='%H:%M'))
    return_time =  CharField(initial= time(18), required=False, widget=TimePickerInput(format='%H:%M'))
    ride_type = CharField(widget=Select(choices=Ride.RIDE_TYPES))
    no_of_seats = CharField(initial=3,widget=NumberInput( attrs={'min':'1','max':'3'}))
 
    def __init__(self, *args, request=None, **kwargs):
        super(RideForm, self).__init__(*args, **kwargs)
        self.request = request
        if self.request:
            self.fields['car'] =  ModelChoiceField(
                required=True,
                queryset=Car.objects.filter(Owner=self.request.user).only("Car_Manufacture", "CarReg_id").all(),
                widget=Select()
                )
            self.fields['restrictions'] = CharField(required=False, widget=TextInput(attrs={'placeholder': 'Ex: No Smoking, ...'}))    
        
            self.fields['area'] = CharField(initial=self.request.user.profile.area,
                widget=Select(choices=self.get_user_areas(self.request.user.profile.city),
                                                            attrs={'id': 'area'}))
            self.fields['city'] = CharField(initial=self.request.user.profile.city,
                widget=Select(choices=RideForm.get_cities(), attrs={'onchange': 'change_areas();','id': 'city'}))
    
    class Meta:
        model = Ride
        fields = [
            'ride_type', 'area', 'no_of_seats','city',
            'restrictions', 'date','car', 'meeting_point', 'leave_time' , 'return_time'
        ]
    field_order = ['ride_type', 'car', 'city', 'area', 'date',
                   'no_of_seats','leave_time', 'return_time', 'meeting_point', 'restrictions']
