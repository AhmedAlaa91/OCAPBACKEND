from __future__ import annotations

import json
from pathlib import Path

from website.models import Ride
from django import forms
from django.forms import CharField, Select, TextInput, BooleanField, CheckboxInput, ModelChoiceField, DateTimeInput, NumberInput
from website.models import Car
from datetime import datetime, timedelta, time

class RideForm(forms.ModelForm):

    def get_initial_start_time():
        tommorow = datetime.today() + timedelta(days=1)
        hour = time(hour=8, minute=0)
        return datetime.combine(tommorow, hour)
    
    def get_initial_return_time():
        tommorow = datetime.today() + timedelta(days=1)
        hour = time(hour=18, minute=0)
        return datetime.combine(tommorow, hour)

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
    
    start_date =  CharField(initial=get_initial_start_time(),widget=DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'class':'datetimefield'}))
    is_ride_two_ways = BooleanField(required=False, label = 'Is your ride 2 ways?', widget=CheckboxInput(attrs={'id': 'is_ride_two_ways'}))
    return_date = CharField(initial=get_initial_return_time(), required=False, widget=DateTimeInput(format='%Y-%m-%dT%H:%M:%S', attrs={'class':'datetimefield','id':'return_datetimefield'}))
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
        
            self.fields['source'] = CharField(initial=self.request.user.profile.area,
                widget=Select(choices=self.get_user_areas(self.request.user.profile.city),
                                                            attrs={'id': 'source'}))
            self.fields['destination'] = CharField(
                widget=Select(choices=self.get_user_areas(self.request.user.profile.city),
                                                            attrs={'id': 'destination'}))

    
    class Meta:
        model = Ride
        fields = [
            'source', 'destination', 'no_of_seats',
            'restrictions', 'start_date', 'return_date','car'
        ]
    field_order = ['source', 'destination', 'no_of_seats', 'start_date',
                    'is_ride_two_ways', 'return_date', 'car', 'restrictions']
