from __future__ import annotations

import json
from pathlib import Path

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField
from django.forms import HiddenInput
from django.forms import ModelForm
from django.forms import Select
from phonenumber_field.formfields import PhoneNumberField
from website.models import Profile


class RegisterForm(UserCreationForm):

    password1 = CharField(widget=HiddenInput(), required=False)

    password2 = CharField(widget=HiddenInput(), required=False)

    def __init__(self, *args, request=None, **kwargs):

        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None

        self.request = request

        if self.request:

            self.user_info = self.request.session.get('user_info')

            self.fields['username'].initial = self.user_info.get('sub')

            self.fields['email'].initial = self.user_info.get('email')

            self.fields['first_name'].initial = self.user_info.get(
                'given_name',
            )

            self.fields['last_name'].initial = self.user_info.get(
                'family_name',
            )

            self.fields['username'].widget.attrs['readonly'] = True

            self.fields['email'].widget.attrs['readonly'] = True

            self.fields['first_name'].widget.attrs['readonly'] = True

            self.fields['last_name'].widget.attrs['readonly'] = True

    class Meta:

        model = User

        fields = ['username', 'email', 'first_name', 'last_name']


class ChangeUserForm(UserChangeForm):

    password1 = CharField(widget=HiddenInput(), required=False)

    password2 = CharField(widget=HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):

        super(UserChangeForm, self).__init__(*args, **kwargs)

        del self.fields['password']

        self.fields['username'].help_text = None

        self.fields['username'].widget.attrs['readonly'] = True

        self.fields['email'].widget.attrs['readonly'] = True

        self.fields['first_name'].widget.attrs['readonly'] = True

        self.fields['last_name'].widget.attrs['readonly'] = True

    class Meta:

        model = User

        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileForm(ModelForm):

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

    phone = PhoneNumberField()

    gender = CharField(widget=Select(choices=Profile.UserGender))

    city = CharField(

        widget=Select(
            choices=get_cities(),

            attrs={'onchange': 'change_areas();', 'id': 'cities'},
        ),
    )

    area = CharField(

        widget=Select(

            choices=[('0', 'Choose Area')],

            attrs={'id': 'areas'},
        ),

    )
    def __init__(self, *args, **kwargs):

        super(ModelForm, self).__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs['autocomplete'] = "off"

    class Meta:

        model = Profile

        fields = ['phone', 'gender', 'city', 'area']
