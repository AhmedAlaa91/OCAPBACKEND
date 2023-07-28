
import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


class CarPlate(models.Model):

    def validate_length(value):
        an_integer = value
        a_string = str(an_integer)
        length = len(a_string)
        if length > 5:
            raise ValidationError(
                _('Plate Number is above 5 digits'),
            )

    CarPlate_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False,
    )
    Number = models.IntegerField(validators=[validate_length], blank=False)
    Letter_one = models.CharField(max_length=1, blank=True)
    Letter_two = models.CharField(max_length=1, blank=False)
    Letter_three = models.CharField(max_length=1, blank=False)

    def __str__(self): return str(self.Number) + ' ' + str(self.Letter_three) + \
        ' ' + str(self.Letter_two) + ' ' + str(self.Letter_one)


class Car(models.Model):
    CarReg_id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False,
    )
    No_OF_Seats = models.IntegerField(max_length=10, default='3')
    Car_Pallet_Number = models.ForeignKey(CarPlate, on_delete=models.CASCADE, related_name='plate')
    Car_Manufacture = models.CharField(max_length=50)
    Car_Color = models.CharField(max_length=50)
    Owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
    )

    def __str__(self): return str(self.Car_Manufacture) + ' - ' + str(self.Car_Color) + ' /  Plate Number : ' + str(
        self.Car_Pallet_Number)
