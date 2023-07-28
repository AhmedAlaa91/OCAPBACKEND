from __future__ import annotations

from django import forms
from apps.website.models import Car
from apps.website.models import CarPlate
# import  from models.py

# create a ModelForm


class CarRegistrationForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Car
        fields = [
            'Car_Manufacture',
            'Car_Color', 'No_OF_Seats',
        ]


class CarPlateForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = CarPlate
        fields = [
            'Number', 'Letter_one', 'Letter_two', 'Letter_three',
        ]
        labels = {
            'Number': '',
            'Letter_one': '',
            'Letter_two': '',
            'Letter_three': '',
        }
