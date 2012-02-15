from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User)
    languages = models.ManyToManyField('Language', blank=True)

    class Meta:
        app_label = 'confucius'


class Address(models.Model):
    account = models.ForeignKey(Account)
    main = models.BooleanField()
    name = models.CharField(max_length=31)

    class Meta:
        abstract = True
        app_label = 'confucius'

    def __unicode__(self):
        return self.value


class EmailAddress(Address):
    value = models.EmailField(unique=True)


class PostalAddress(Address):
    value = models.TextField()


class Language(models.Model):
    code = models.CharField(max_length=5, choices=settings.LANGUAGES)

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.code
