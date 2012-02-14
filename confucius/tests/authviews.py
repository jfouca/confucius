from django.utils import unittest
from django.test.client import Client

from confucius.models import User


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        u = User.objects.create(
                username="blu", password="blu", last_name="blu",
                email="blu@blu.fr")
        u.set_password("blu")
        u.save()
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        self.assertTrue(self.client.login(username="blu", password="blu"))
