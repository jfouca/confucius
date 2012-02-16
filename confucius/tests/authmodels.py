from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import unittest

from confucius.models import Account
from confucius.utils import email_to_username


class AccountTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }

    def setUp(self):
        Account.objects.all().delete()

    def test_create(self):
        account = Account.objects.create(**self.sample_info)

        self.assertIsInstance(User.objects.get(pk=account.user_id), User)
        self.assertTrue(account.check_password(self.sample_info['password']))
        self.assertFalse(account.is_active)
        self.assertEquals(account.username,
            email_to_username(self.sample_info['email']))

        self.assertIsInstance(Account.objects.get(pk=account.pk), Account)
        self.assertEquals(Account.objects.filter(
            emailaddress__value__exact=self.sample_info['email']).count(),
            1)

    def test_create_already_existing(self):
        Account.objects.create(**self.sample_info)
        self.assertRaises(IntegrityError, lambda: Account.objects.create(**self.sample_info))

    def test_add_email(self):
        account = Account.objects.create(**self.sample_info)
        email = 'bob@alice.com'

        account.add_email(email)
        self.assertEquals(
            account.emailaddress_set.get(value=email).value, email)
