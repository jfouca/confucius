from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import unittest

from confucius.models import Account, EmailAddress
from confucius.utils import email_to_username


class AccountTestCase(unittest.TestCase):
    sample_info = {
        'email': 'alice@bob.com',
        'last_name': 'Blu',
        'password': 'red',
    }
    sample_email = 'bob@alice.com'

    def setUp(self):
        Account.objects.all().delete()
        self.account = Account.objects.create(**self.sample_info)

    def test_create(self):
        self.assertIsInstance(User.objects.get(pk=self.account.user_id), User)
        self.assertTrue(self.account.check_password(
            self.sample_info['password']))
        self.assertFalse(self.account.is_active)
        self.assertEquals(self.account.username,
            email_to_username(self.sample_info['email']))

        self.assertIsInstance(Account.objects.get(pk=self.account.pk), Account)
        self.assertEquals(Account.objects.filter(
            emailaddress__value__exact=self.sample_info['email']).count(),
            1)

        self.assertRaises(IntegrityError,
            lambda: Account.objects.create(**self.sample_info))

        self.account.delete()
        self.assertEquals(Account.objects.count(), 0)
        self.assertEquals(EmailAddress.objects.count(), 0)
        self.assertEquals(User.objects.count(), 0)

    def test_multiple_create(self):
        for i in range(127):
            Account.objects.create(email='test' + str(i) + '@test.com',
                password='test', last_name='test')
        self.assertEquals(Account.objects.count(), 128)
        self.assertEquals(EmailAddress.objects.count(), 128)
        self.assertEquals(User.objects.count(), 128)
        Account.objects.all().delete()
        self.assertEquals(Account.objects.count(), 0)
        self.assertEquals(EmailAddress.objects.count(), 0)
        self.assertEquals(User.objects.count(), 0)

    def test_get_by_email(self):
        account = Account.objects.get_by_email(self.sample_info['email'])

        self.assertEquals(account.last_name, self.sample_info['last_name'])
        self.assertRaises(Account.DoesNotExist,
                lambda: Account.objects.get_by_email('duran@duran.com'))

    def test_add_email(self):
        self.account.add_email(self.sample_email)
        self.assertEquals(
            self.account.emailaddress_set.get(value=self.sample_email).value,
            self.sample_email)
        self.assertRaises(IntegrityError,
                lambda: self.account.add_email(self.sample_info['email']))

    def test_has_email(self):
        self.account.add_email('test@test.com')
        self.account.add_email(self.sample_email)
        self.account.add_email('blu@red.com')
        self.assertTrue(self.account.has_email(self.sample_email))
        self.assertFalse(self.account.has_email('duran@duran.com'))
