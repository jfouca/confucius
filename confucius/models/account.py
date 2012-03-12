from django.contrib.auth.models import User as AuthUser
from django.db import models

from confucius.models import ConfuciusModel


# Monkeypatch
del AuthUser.get_absolute_url


class User(AuthUser):
    class Meta:
        proxy = True

    def __unicode__(self):
        return self.email

    def get_last_accessed_conference(self):
        try:
            membership = self.memberships.get(last_accessed=True)
            return membership.conference
        except:
            pass

        return None

    def has_chair_role_in_any_conference(self):
        memberships = self.memberships
        for member in memberships.all():
            if member.has_chair_role():
                return True
        return False


class Activation(ConfuciusModel):
    activation_key = models.CharField(max_length=64, unique=True)
    email = models.ForeignKey('Email', unique=True)

    def save(self, *args, **kwargs):
        from hashlib import sha256
        from confucius.utils import random_string

        if self.activation_key == '':
            self.activation_key = sha256(random_string()).hexdigest()

        super(Activation, self).save(*args, **kwargs)

    def send_email(self, domain):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string

        context = {'activation_key': self.activation_key, 'domain': domain}
        message = render_to_string('account/confirm_email.html', context)

        send_mail('Email confirmation', message, None, [self.email.value])


class Email(ConfuciusModel):
    user = models.ForeignKey(User, related_name='emails')
    confirmed = models.BooleanField(default=False)
    main = models.BooleanField(default=False)
    value = models.EmailField(unique=True, verbose_name='email')

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
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name
