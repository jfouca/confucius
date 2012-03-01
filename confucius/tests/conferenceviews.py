from django.utils import unittest
from confucius.models import Conference, Alert, Role, ConferenceAccountRole, Account
from django.test.client import Client

class conferenceviewsTestCase(unittest.TestCase):

    def setUp(self):
        self.account_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
        }
        self.role_info = {
        'code': 'PRES',
        'name': 'president',
        }
        Role.objects.all().delete()
        Conference.objects.all().delete()
        Account.objects.all().delete()
        ConferenceAccountRole.objects.all().delete()
        Alert.objects.all().delete()
        self.account = Account.objects.create(**self.account_info)
        self.account.save()
        self.role = Role.objects.create(**self.role_info)
        self.role.save()
        
        self.client = Client()


    def test_succesfull_create_conference(self):
        response = self.client.get('/conf-create/')
        response = self.client.post('/conf-create/',
            {'owner_account_id': self.account.pk,
            'conference_title': "My conference"})
        self.assertEquals(302, response.status_code)
