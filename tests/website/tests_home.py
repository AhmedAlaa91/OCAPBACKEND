from django.test import TestCase, Client
from django.urls import reverse


class HomeTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        url = reverse('pages.home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
