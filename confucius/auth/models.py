from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User)
    secondary_email = models.EmailField()
    primary_postal_address = models.TextField()
    secondary_postal_address = models.TextField() 
    languages = models.ManyToManyField("Language")

class Language(models.Model):
    code = models.CharField(max_length=2)
    value = models.CharField(max_length=40)

    

