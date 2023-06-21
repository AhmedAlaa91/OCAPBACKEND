from __future__ import annotations

from django import forms
from website.models import Car
# import  from models.py

# create a ModelForm


class CarRegistrationForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Car
        fields = [
            'Car_Pallet_Number', 'Car_Manufacture',
            'Car_Color', 'No_OF_Seats',
        ]
