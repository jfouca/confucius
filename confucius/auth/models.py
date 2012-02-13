from django.contrib.auth.models import User
from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User)
    secondary_email = models.EmailField(blank=True)
    primary_postal_address = models.TextField()
    secondary_postal_address = models.TextField(blank=True)
    languages = models.ManyToManyField(Language)
