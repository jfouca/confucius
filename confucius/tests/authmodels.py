from django.utils import unittest
from django.core.exceptions import ValidationError

from confucius.models import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        User.objects.all().delete()

    def test_missing_arguments(self):
        self.assertRaises(ValidationError, lambda: User.objects.create())
        self.assertRaises(ValidationError,
                lambda: User.objects.create(username="test"))
        self.assertRaises(ValidationError,
                lambda: User.objects.create(username="foo", password="bar"))
        self.assertRaises(ValidationError,
                lambda: User.objects.create(
                    username="ni", password="rah", last_name="mit"))
        self.assertRaises(ValidationError,
                lambda: User.objects.create(
                    username="blu", password="red", last_name="sky"))

    def test_unicity(self):
        u = User.objects.create(
                username="user1", password="doesntmatter", last_name="user1",
                email="user1@user1.com")
        u.pk = None
        self.assertRaises(ValidationError,
                lambda: u.save())
        u.pk = None
        u.username = "user2"
        self.assertRaises(ValidationError,
                lambda: u.save())
        u.pk = None
        u.username = "user1"
        u.email = "user2@user2.com"
        self.assertRaises(ValidationError,
                lambda: u.save())
