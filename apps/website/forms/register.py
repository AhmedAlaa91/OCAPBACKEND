from __future__ import annotations

from apps.website.jsonData import JsonData
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
 
    phone = PhoneNumberField()

    gender = CharField(widget=Select(choices=Profile.UserGender))

    city = CharField(required=False,

        widget=Select(
            choices=JsonData.get_cities(),

            attrs={'onchange': 'change_areas();', 'id': 'cities'},
        ),
    )

    area = CharField(required=False,

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
