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

    def save(self, *args, **kwargs):
        try:
            self.user
        except User.DoesNotExist:
            import base64
            u = User(username=base64.b64encode(self.email_addresses.all()[0].value))
            u.save()
            self.user = u

        super(Profile, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.first_name +" "+ self.last_name+" <"+self.email_addresses.all()[0].value+">"
  
