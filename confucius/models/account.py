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


class Activation(ConfuciusModel):
    activation_key = models.CharField(max_length=64, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    email = models.ForeignKey('Email', unique=True)

    def has_expired(self):
        import datetime

        expiration_date = self.date + datetime.timedelta(days=1)
        if datetime.datetime.now() >= expiration_date:
            return True
        return False

    def clean(self):
        from hashlib import sha256
        from confucius.utils import random_string

        if self.activation_key is None:
            self.activation_key = sha256(random_string()).hexdigest()

        super(Activation, self).clean()

    def send_email(self):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string

        context = {'activation_key': self.activation_key}
        message = render_to_string('registration/activation_email.html', context)

        send_mail('Email confirmation', message, None, (unicode(self.email),))


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
        from hashlib import sha256
        from confucius.utils import email_to_username, random_string

        if self.pk is None:
            self.activation_key = sha256(random_string()).hexdigest()

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
