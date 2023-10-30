from django.test import TestCase , Client
from django.urls import reverse
import pytest
from apps.website.models import CarRegistration

from apps.website.Serilaizers.Rides_serializer import car_serializer
class CarsTest(TestCase):
    
   
    def test_get_cars_query(self):
        requests = CarRegistration.Car.objects.all()

    
        self.assertEqual(requests.count(), 3)

    
    def test_get_cars_api(self):
        client = Client()
        request = client.get(reverse ('cars'))

        self.assertEqual(request.status_code, 200)