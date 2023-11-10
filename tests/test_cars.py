from django.test import TestCase , Client
from django.urls import reverse
from apps.website.models import CarRegistration

class CarsTest(TestCase):
    
   
    def test_get_cars_query(self):
        requests = CarRegistration.Car.objects.all()
        self.assertEqual(requests.count(), 3)

    
    def test_get_cars_api(self):
        client = Client()
        request = client.get(reverse ('cars'))
        self.assertEqual(request.status_code, 200)