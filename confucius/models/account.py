from django.contrib.auth.models import User
from django.db import models

from confucius.models import ConfuciusModel


class Email(ConfuciusModel):
    user = models.ForeignKey(User, related_name='emails')
    confirmed = models.BooleanField(default=False)
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


class EmailSignup(ConfuciusModel):
    date = models.DateTimeField(auto_now=True)
    activation_key = models.CharField(max_length=40)
    email = models.ForeignKey(Email)

    def has_expired(self):
        import datetime

        expiration_date = self.date + datetime.timedelta(days=1)
        if datetime.datetime.now() >= expiration_date:
            return True
        return False

    def send_activation_email(self):
        from django.core.mail import send_mail
        from django.middleware.csrf import _get_new_csrf_key
        from django.template.loader import render_to_string

        self.activation_key = _get_new_csrf_key()
        context = {'activation_key': self.activation_key}
        message = render_to_string('registration/activation_email.html', context)

        send_mail('Email confirmation', message, None, (unicode(self.email),))


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
