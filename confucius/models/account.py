from django.contrib.auth.models import User
from django.db import models

from confucius.models import ConfuciusModel


class Email(ConfuciusModel):
    user = models.ForeignKey(User, related_name='emails')
    main = models.BooleanField(default=False)
    value = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        """
        When saved, if self is a main address it should update the User's email
        with its value.
        """
        from confucius.utils import email_to_username

        super(Email, self).save(*args, **kwargs)

        if self.main:
            self.user.email = self.value
            self.user.username = email_to_username(self.value)
            self.user.save()

    def __unicode__(self):
        return self.value


class Address(ConfuciusModel):
    user = models.ForeignKey(User, related_name='addresses')
    value = models.TextField(verbose_name='address')

    def __unicode__(self):
        return self.value


class Language(ConfuciusModel):
    users = models.ManyToManyField(User, related_name='languages')
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name
