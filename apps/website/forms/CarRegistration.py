from __future__ import annotations

from django import forms
from apps.website.models import Car
from apps.website.models import CarPlate

from apps.website.jsonData import JsonData



# import  from models.py

# create a ModelForm


class CarRegistrationForm(forms.ModelForm):
    # specify the name of model to use
    car_brands = JsonData.get_carbrand()
    Car_Manufacture= forms.CharField(label='Brand', widget=forms.Select(choices=car_brands))

    all_colors = JsonData.get_carcolor()
    Car_Color= forms.CharField(label='Color', widget=forms.Select(choices=all_colors))

    No_OF_Seats = forms.CharField(initial=3, widget=forms.NumberInput(attrs={'min': '1', 'max': '3'}))
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
