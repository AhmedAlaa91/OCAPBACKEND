from __future__ import annotations

from django import forms

from apps.website.jsonData import JsonData
from apps.website.models import Car, CarPlate

# import  from models.py

# create a ModelForm


class CarRegistrationForm(forms.ModelForm):
    # specify the name of model to use
    car_brands = JsonData.get_carbrand()
    Car_Manufacture = forms.CharField(label="Brand", widget=forms.Select(choices=car_brands))

    all_colors = JsonData.get_carcolor()
    Car_Color = forms.CharField(label="Color", widget=forms.Select(choices=all_colors))

    No_OF_Seats = forms.CharField(initial=3, widget=forms.NumberInput(attrs={"min": "1", "max": "3"}))

    No_OF_Seats = forms.CharField(initial=3, widget=forms.NumberInput(attrs={'min': '1', 'max': '3'}))
    Car_license =forms.BooleanField(label='Is Car license Valid ?',required=False)
    Driver_license = forms.BooleanField(label='Is Driver license Valid ?',required=False)

    class Meta:
        model = Car
        fields = [
            'Car_Manufacture',
            'Car_Color', 'No_OF_Seats','Car_license','Driver_license','Engine_size','No_clyender','Fuel_consumption'
        ]


class CarPlateForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = CarPlate
        fields = [
            "Number",
            "Letter_one",
            "Letter_two",
            "Letter_three",
        ]
        labels = {
            "Number": "",
            "Letter_one": "",
            "Letter_two": "",
            "Letter_three": "",
        }
