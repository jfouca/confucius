from django.contrib.auth.models import User
from django.db import models


class PostalAddress(models.Model):
    profile = models.ForeignKey('Profile', related_name='postal_addresses')
    name = models.CharField(max_length=32, verbose_name="label")
    value = models.TextField(verbose_name="address")

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.value


class EmailAddress(models.Model):
    profile = models.ForeignKey('Profile', related_name='email_addresses')
    name = models.CharField(max_length=32, verbose_name="label")
    value = models.EmailField(unique=True, verbose_name="Email")

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.value


class Language(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=40)

    class Meta:
        app_label = "confucius"

    def __unicode__(self):
        return self.name


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    languages = models.ManyToManyField(Language, blank=True)

    class Meta:
        app_label = "confucius"
                
    def __unicode__(self):
        return self.first_name +" "+ self.last_name+" <"+self.email_addresses.all()[0].value+">"



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        p = Profile.objects.create(user=instance)
        EmailAddress.objects.create(name="main address",
                value=instance.email, profile=p)

models.signals.post_save.connect(create_user_profile, sender=User)

