from __future__ import annotations

from datetime import datetime, time, timedelta

from django import forms
from django.forms import CharField, ModelChoiceField, NumberInput, Select, TextInput

from apps.website.models import Car, Ride

from .widgets import DatePickerInput, TimePickerInput


def get_initial_date():
    date = datetime.today() + timedelta(days=1)
    return date


class RideForm(forms.ModelForm):
    date = CharField(initial=get_initial_date(), widget=DatePickerInput(format="%Y-%m-%d"))
    leave_time = CharField(initial=time(8), widget=TimePickerInput(format="%H:%M"))
    return_time = CharField(initial=time(18), required=False, widget=TimePickerInput(format="%H:%M"))
    ride_type = CharField(widget=Select(choices=Ride.RIDE_TYPES))
    no_of_seats = CharField(initial=3, widget=NumberInput(attrs={"min": "1", "max": "3"}))

    def __init__(self, *args, request=None, **kwargs):
        super(RideForm, self).__init__(*args, **kwargs)
        self.request = request
        if self.request:
            self.fields["car"] = ModelChoiceField(
                required=True,
                queryset=Car.objects.filter(Owner=self.request.user)
                .only("Car_Manufacture", "CarReg_id")
                .all(),
                widget=Select(),
            )
            self.fields["restrictions"] = CharField(
                required=False, widget=TextInput(attrs={"placeholder": "Ex: No Smoking, ..."})
            )

            self.fields["area"] = CharField(
                required=True, widget=Select(choices=[("", "Choose Area")], attrs={"id": "areas"})
            )
            self.fields["city"] = CharField(
                required=True,
                widget=Select(
                    choices=[("", "Choose City")], attrs={"onchange": "change_areas();", "id": "cities"}
                ),
            )

    class Meta:
        model = Ride
        fields = [
            "ride_type",
            "area",
            "no_of_seats",
            "city",
            "restrictions",
            "date",
            "car",
            "meeting_point",
            "leave_time",
            "return_time",
        ]

    field_order = [
        "ride_type",
        "car",
        "city",
        "area",
        "date",
        "no_of_seats",
        "leave_time",
        "return_time",
        "meeting_point",
        "restrictions",
    ]
