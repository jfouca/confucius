from django.utils import unittest
from django.test.client import Client

from confucius.models import Account


# NEED SOME HEAVY REWRITING

class LoginTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    sample_email = 'bob@alice.com'

    def setUp(self):
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.client = Client()

    def test_succesfull_login(self):
        response = self.client.post('/login/',
            {'username': self.sample_info['email'],
            'password': self.sample_info['password']})

        self.assertEquals(200, response.status_code)

"""
    def test_empty_username_login(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        self.assertFalse(self.client.login(username="", password="blu"))

    def test_empty_password_login(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        self.assertFalse(self.client.login(username="blu", password=""))

    def test_wrong_username_login(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        self.assertFalse(self.client.login(username="bla", password="blu"))

    def test_wrong_password_login(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        self.assertFalse(self.client.login(username="blu", password="bla"))
"""


class PasswordChangeTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    sample_email = 'bob@alice.com'

    def setUp(self):
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.client = Client()

    def test_change_password(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        #self.client.post('/change-password/',{'old_password':'blu','new_password1':'bla','new_password2':'bla'})


class LogoutTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    sample_email = 'bob@alice.com'

    def setUp(self):
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)
        self.client = Client()
    
    def test_successfull_logout(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
