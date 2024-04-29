from django.test import TestCase
from django.urls import reverse
# Create your tests here.

class PageConnectionTest(TestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)