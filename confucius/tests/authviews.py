from django.utils import unittest
from django.test.client import Client
from confucius.models import User


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        #Creating a mock webClient
        self.client = Client()
        #Deleting all user in database before creating our test_user blu
        User.objects.all().delete()
        u = User.objects.create(
                username="blu", password="blu", last_name="blu",
                email="blu@blu.fr")
        u.set_password("blu")
        u.save()

    def test_succesfull_login(self):
        response = self.client.get('/login/')
        self.assertEquals(200, response.status_code)
        self.assertTrue(self.client.login(username="blu", password="blu"))

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

class PasswordTestCase(unittest.TestCase):
    def setUp(self):
        #Creating a mock webClient
	self.client = Client()
        #Deleting all user in database before creating our test_user blu
        User.objects.all().delete()
        u = User.objects.create(username="blu", password="blu", last_name="blu",email="blu@blu.fr")
    	u.set_password("blu")
     	u.save()

    def test_change_password(self):
	response = self.client.get('/login/')
	self.assertEquals(200, response.status_code)
	self.client.login(username="blu", password="blu")
	self.client.post('/change-password/',{'old_password':'blu','new_password1':'bla','new_password2':'bla'})
     	self.assertTrue(u.check_password('bla'))
